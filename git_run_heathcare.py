from openai import OpenAI
import pandas as pd
from tqdm import tqdm
import google.generativeai as genai
import anthropic
import ast
import time

genai.configure(api_key="GOOGLE_API_KEY")

claude_client = anthropic.Anthropic(api_key="ANTHROPIC_API_KEY")

client = OpenAI(api_key="OPENAI_API_KEY")

system_content = ""
user_content = """\nI want your response to be formatted as json like this:{"effectiveness":"scale"}"""

def claude_get_response(system_content, user_content_query, max_retries=3):
    for attempt in range(max_retries):
        try:
            message = claude_client.messages.create(
                model="claude-3-5-sonnet-20240620",  
                max_tokens=1000,
                temperature=1.0,
                system=system_content,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": user_content_query,
                            }
                        ]
                    }
                ]
            )
            return message.content[0].text
        except anthropic.RateLimitError as e:
            print(f"Claude rate limit hit, attempt {attempt + 1}/{max_retries}")
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 30
                print(f"Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                print("Claude: Max retries reached, skipping this request")
                return '{"effectiveness":"ERROR: Rate limit exceeded"}'
        except Exception as e:
            print(f"Claude error: {e}")
            return f'{{"effectiveness":"ERROR: {str(e)}"}}'

def gemini_get_response(system_content, user_content_query, max_retries=3):
    """
    Sends a request to the Gemini API and returns the generated headline.
    """
    for attempt in range(max_retries):
        try:
            model = genai.GenerativeModel(
                model_name="gemini-1.5-pro",
                system_instruction=system_content
            )
            
            generation_config = genai.types.GenerationConfig(
                temperature=1.0
            )

            response = model.generate_content(
                user_content_query,
                generation_config=generation_config
            )
            r = response.text.replace("```json\n","").replace("```","")
            return r
        except Exception as e:
            print(f"Gemini error attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(10)
            else:
                return f'{{"effectiveness":"ERROR: {str(e)}"}}'

def chatgpt_get_response(system_content, user_content_query, max_retries=3):
    for attempt in range(max_retries):
        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=1.0,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": user_content_query}
                ]
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"ChatGPT error attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(10)
            else:
                return f'{{"effectiveness":"ERROR: {str(e)}"}}'


medical_records = pd.read_excel('YOUR_FILE_NAME', sheet_name=0)


# Add new columns for the results
medical_records['claude_results'] = None
medical_records['gemini_results'] = None
medical_records['chatgpt_results'] = None

print(f"Processing {len(medical_records)} rows (starting from row 2)...")

# Process one row at a time and save results
for idx, (index, row) in enumerate(tqdm(medical_records.iterrows(), total=len(medical_records))):
    print(f"\Processing row {index} ({idx+1}/{len(medical_records)})...")
    
    
    cause = row['Cause']
    effect = row['Effect']
    
    local_list = ast.literal_eval(row['gen_medical_records'])
    
    
    claude_scores = []
    gemini_scores = []
    chatgpt_scores = []
    
    for k, v in local_list.items():
        comb_lista = []
        for lista in v:
            lista = ast.literal_eval(lista)
            comb = f'{cause}:{lista[0]}, {effect}:{lista[1]}'
            comb_lista.append(comb)
        
        
        query = " .These are the medical records:" + str(comb_lista) + user_content
        
        print(f"  Processing combination {k}...")
        
        
        claude_result = claude_get_response(row['Prompt'], query)
        claude_scores.append(claude_result)
        time.sleep(2)
        
        gemini_result = gemini_get_response(row['Prompt'], query)
        gemini_scores.append(gemini_result)
        time.sleep(2)
        
        chatgpt_result = chatgpt_get_response(row['Prompt'], query)
        chatgpt_scores.append(chatgpt_result)
        time.sleep(2)
    
    # Save the results in DataFrame
    medical_records.at[index, 'claude_results'] = str(claude_scores)
    medical_records.at[index, 'gemini_results'] = str(gemini_scores)
    medical_records.at[index, 'chatgpt_results'] = str(chatgpt_scores)
    

    # Save the updated DataFrame
    medical_records.to_excel('medical_records_with_results.xlsx', index=False)
    print(f"  Row {index} completed and saved")

print("\n Process completed")
print("Results saved in: medical_records_with_results.xlsx")

