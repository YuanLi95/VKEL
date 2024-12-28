import json
import openai
from openai import OpenAI
import requests
import base64
import os
from zhipuai import ZhipuAI

# os.environ["OPENAI_BASE_URL"] = "https://4.0.wokaai.com/v1/"
os.environ["OPENAI_BASE_URL"] = "https://uiuiapi.com/v1"
# model = 'gpt-3.5-turbo'
model = "claude-3-5-sonnet-20240620"
# model = "llama-2-70b"
# model = "llama3-70b-8192"
# model = "gpt-3.5-turbo"
model = "gemini-pro"
model = "gpt-4o-mini"
model = "gpt-4"
need_img = False
if need_img:
    suffix = '_with_img'
else:
    suffix = ''

client_gpt = OpenAI(
    api_key="sk-yQFtYnyaM40ze5Te6dEaD453318a49Ec89694b25985dD392" #"https://uiuiapi.com/v1
    # api_key ="sk-YmMgAlBKJ4m8ypsz517a963258Af4c0c963c4fBe128735Ea"
)

#Person
base_prompt = {"person":"You possess extensive world knowledge. I will provide the Person (coarse type) named '{0}' and a corresponding sentence: '{1}' (sentence). Based on your knowledge, choose the most appropriate specific type from ['politician', 'musician', 'actor', 'artist', 'athlete', 'author', 'businessman', 'character', 'coach', 'director', 'intellectual', 'journalist', 'person_other'], and use your stored knowledge to briefly describe the following aspects of the Person so I can identify this coarse type from a picture without needing additional description. Each aspect is only one sentence.: \n1. Type: \n2. Man or Women: \n3. Facial contour: \n4. Hairstyle: \n5. Skin color: \n6. Whether the clothes are in a special number, if he has please answer the number, not has to answer No:",
          "organization":"You possess extensive world knowledge. I will provide an organization (coarse type) named '{0}' and a corresponding sentence: '{1}' (sentence). Based on your knowledge, choose the most appropriate specific type from ['company', 'educational institution', 'band', 'government agency'], and use your stored knowledge to briefly describe the following aspects of the organization so I can identify this coarse type from a picture without needing additional description. Each aspect is only one sentence. \n1. Type:\n2. Team logo and emblem:\n3. Slogan:",
          "product":"You possess extensive world knowledge. I will provide the Product (coarse type) named '{0}' and a corresponding sentence: '{1}' (sentence). Based on your knowledge, choose the most appropriate specific type from ['brand_name_products','game','product_other','software'], and use your stored knowledge to briefly describe the following aspects of the Product so I can identify this coarse type from a picture without needing additional description. Each aspect is only one sentence.\n1. Type:\n2. Brand and trademark:\n3. Product name:\n4. Product appearance features:\n5. Product materials:",
          "building":"You possess extensive world knowledge. I will provide the Building (coarse type) named '{0}' and a corresponding sentence: '{1}' (sentence).Based on your knowledge, choose the most appropriate specific type from ['building_other','cultural_place','entertainment_place','sports_facility'], and use your stored knowledge to briefly describe the following aspects of the Building so I can identify this coarse type from a picture without needing additional description. Each aspect is only one sentence.\n1. Type:\n2. Address:\n3. Appearance:\n4. Building materials:",
          "event":"You possess extensive world knowledge. I will provide the Event (coarse type) named '{0}' and a corresponding sentence: '{1}' (sentence).Based on your knowledge, choose the most appropriate specific type from ['event_other','festival','sports_event'], , and use your stored knowledge to briefly describe the following aspects of the Building so I can identify this coarse type from a picture without needing additional description. Each aspect is only one sentence.\n1. Type:\n2. Appearance:\n3. Background:",
          "other":"You possess extensive world knowledge. I will provide the Other (coarse type) named '{0}' and a corresponding sentence: '{1}' (sentence).Based on your knowledge, choose the most appropriate specific type from ['animal','award','medical_thing','website','ordinance'], , and use your stored knowledge to briefly describe the following aspects of the Building so I can identify this coarse type from a picture without needing additional description. Each aspect is only one sentence.\n1. Type:\n2. Appearance:\n3. Background:",
          "art":"You possess extensive world knowledge. I will provide the Art (coarse type) named '{0}' and a corresponding sentence: '{1}' (sentence).Based on your knowledge, choose the most appropriate specific type from ['art_other','film_and_television_works','magazine','music','written_work'], , and use your stored knowledge to briefly describe the following aspects of the Building so I can identify this coarse type from a picture without needing additional description. Each aspect is only one sentence.\n1. Type:\n2. Appearance:\n3. Background:",
          "location":"You possess extensive world knowledge. I will provide the Location (coarse type) named '{0}' and a corresponding sentence: '{1}' (sentence).Based on your knowledge, choose the most appropriate specific type from ['city','country','state','continent','location_other','park','road'], , and use your stored knowledge to briefly describe the following aspects of the Building so I can identify this coarse type from a picture without needing additional description. Each aspect is only one sentence.\n1. Type:\n2.location: \n3. Logo: \n4. National Flag: \n5. Appearance:\n6. Background:"
          }


coarse_to_fine = {
'location': ['city','country','state','continent','location_other','park','road'],
'building': ['building_other','cultural_place','entertainment_place','sports_facility'],
'organization': ['company','educational_institution', 'band','government_agency',
'news_agency','organization_other','political_party','social_organization','sports_league',
'sports_team'],
'person': ['politician','musician','actor','artist','athlete','author','businessman','character',
'coach','director','intellectual', 'journalist','person_other'],
'other': ['animal','award','medical_thing','website','ordinance'],
'art': ['art_other','film_and_television_works','magazine','music','written_work'],
'event': ['event_other','festival','sports_event'],
'product': ['brand_name_products','game','product_other','software']
}
fine_to_coarse ={
'city': 'location', 'country': 'location', 'state': 'location', 'continent': 'location', 'location_other': 'location', 'park': 'location', 'road': 'location', 'building_other': 'building', 'cultural_place': 'building', 'entertainment_place': 'building', 'sports_facility': 'building', 'company': 'organization', 'educational_institution': 'organization', 'band': 'organization', 'government_agency': 'organization', 'news_agency': 'organization', 'organization_other': 'organization', 'political_party': 'organization', 'social_organization': 'organization', 'sports_league': 'organization', 'sports_team': 'organization', 'politician': 'person', 'musician': 'person', 'actor': 'person', 'artist': 'person', 'athlete': 'person', 'author': 'person', 'businessman': 'person', 'character': 'person', 'coach': 'person', 'director': 'person', 'intellectual': 'person', 'journalist': 'person', 'person_other': 'person', 'animal': 'other', 'award': 'other', 'medical_thing': 'other', 'website': 'other', 'ordinance': 'other', 'art_other': 'art', 'film_and_television_works': 'art', 'magazine': 'art', 'music': 'art', 'written_work': 'art', 'event_other': 'event', 'festival': 'event', 'sports_event': 'event', 'brand_name_products': 'product', 'game': 'product', 'product_other': 'product', 'software': 'product'
}
def getPrompt(sentence, name, fine_type):
    # print(fine_type)
    coarse_type = fine_to_coarse[fine_type]
    # print(coarse_type)
    original_prompt = base_prompt[coarse_type]
    new_prompt = original_prompt.format(name,sentence)
    # print(original_prompt)
    return new_prompt




def getNewContentByGLM4(prompt):
    response = client_glm.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {"role": "user", "content": "{}".format(prompt)},
        ],
    )
    return response.choices[0].message.content


def getNewContentWithImgByGLM4(data):
    image_path = os.path.join('./image/', data['img_id'])
    base64_image = encode_image(image_path)
    response = client_glm.chat.completions.create(
        model="glm-4v",  # 填写需要调用的模型名称
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "{}".format(data['prompt'])
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    )
    return response.choices[0].message.content


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def getNewContent(data, model=''):
    # model = 'gpt-4-turbo-2024-04-09'
    response = client_gpt.chat.completions.create(
        model="{}".format(model),  # 填写需要调用的模型名称
        messages=[
            {"role": "user", "content": "{}".format(data)},
        ],
    )
    return response.choices[0].message.content


def getNewContentWithImg(data, model='gpt4-o'):
    image_path = os.path.join('./image/', data['img_id'])
    base64_image = encode_image(image_path)
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "{}".format(data['prompt'])},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"
                    }
                }
            ]
        }
    ]
    response = client_gpt.chat.completions.create(
        model="{}".format(model),
        messages=messages
    )
    return response.choices[0].message.content



with open('./dev.txt', 'r', encoding='utf-8') as f:
    data = f.readlines()

for item in data:
    print(item)
    exit()

# new_f = open('./knowledge/dev_{}.json'.format(model), 'a+',encoding='utf-8')
#
# with open('./knowledge/dev_{}.json'.format(model), 'r', encoding='utf-8') as f:
#     new_data = f.readlines()
#     number = len(new_data)
#
# for item in data[number:]:
#     print(item)
#     original_item = item.rstrip()
#     knowledge_dict = {}
#     sentence,label_list,image_id = item.strip().split('####')
#     label_list = eval(label_list)
#     for label in label_list:
#         print(label)
#         name, type = label[0], label[1]
#         prompt = getPrompt(sentence,name, type)
#         new_content = getNewContent(prompt, model)
#         knowledge_dict[name] = new_content
#
#     original_item= original_item+"####"+str(knowledge_dict)
#     print(original_item)
#     new_f.write(original_item)
#     new_f.write('\n')
#
