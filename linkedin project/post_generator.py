from llm import llm

def get_len(length):
    if length=="Short":
        return "1 to 5 lines"
    if length=="Medium":
        return "6 to 10 lines"
    if length=="Long":
        return "11 to 15 lines"         

def generate_post(length, Language, topic ):
    promt =  f'''

    Generate a Linkedin post using the belw information. No preamble.

    1) Topic: {topic}
    2) Legth: {length}
    3) Language : {Language}

    If the Language is Hinglish then it means it is a mix of Hindi and English.
    The script for the generated post should always be in English.
    Also add some emojis related to the topic or the post generated

    '''
    response  = llm.invoke(promt)
    return response.content 


if __name__ == '__main__':
    post = generate_post("Short", "English", "Job Search")
    print(post)