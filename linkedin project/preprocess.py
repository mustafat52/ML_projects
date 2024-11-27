import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm import llm




def process_posts(raw_file_path, processed_file_path="data/processed_posts.json"):

    with open(raw_file_path, encoding='utf-8') as file:
        
        enriched_post = []
        
        posts = json.load(file)
        print(posts) 


        for post in posts:

            metadata = extract_metadata(post['text'])
            post_with_metadata = post | metadata

            enriched_post.append(post_with_metadata)


    unified_tags = get_uified_tags(enriched_post)
    for epost in enriched_post:
        current_tags = epost.get('tags', [])  # Use get() to handle missing keys gracefully
        new_tags = {unified_tags[tag] for tag in current_tags if tag in unified_tags}
        epost['tags'] = list(new_tags)



    with open(processed_file_path, encoding='utf-8', mode='w') as outfile:
        json.dump(enriched_post, outfile, indent=4)        


def get_uified_tags(post_with_metadata):

    unique_tags = set()

    for post in post_with_metadata:

        unique_tags.update(post['tags'])


    unique_tags_list = ','.join(unique_tags)

    template = ''' I will give you a list of tags. You need to unify taga with the following requirements,
    1. Tags are unified and merged to create a shorter list.
        Example 1: "Jobseekers", "Job Hunting" can be all merged into a single tag "Job Search".
        Example 2: "Motivation", "Inspiration", "Drive" can be mapped to "Motivation".
        Example 3: "Personal Growth", "Personal Development", "Self Improvement" can be mapped to "Selp Improvemnet"
        Example 4: "Scam Alert", "Job Scam" etc can be mapped to "Scams".

    2. Each tag should be follow title case convention, example: "Motivation", "Job Search"
    3. output should be a JSON object , No preamble. 
    4. Output should have mapping of original tags and the unified tag.
       for example: {{"Jobseekers":"Job Search", "Job Hunting":"Job Search", "Motivaion":"MOtivation","Inspiration"}}


    Here is the list of tags:
    {tags}       
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={'tags':str(unique_tags_list)})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Content too big. Unable to parse jobs")
    return res              


   






def extract_metadata(post):

    template = '''
    
    You are givem a Linkedin post. You need to extract number of lines, language of the post and tags.
    1. Return a valid JSON. No preamble.
    2. JSON object should have exactly three keys: line_count, language and tags.
    3. tags is an array of text tags. Etract maximum two tags.
    4. Language should be English or Hinglish(Hinglish mean Hindi + English)
    

    Here is the actual post on which you need to perform this task:
    {post}
    
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={'post':post})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Content too big. Unable to parse jobs")
    return res
     

    














if __name__ == "__main__":

    process_posts("data/raw_posts.json", "data/processed_posts.json")
