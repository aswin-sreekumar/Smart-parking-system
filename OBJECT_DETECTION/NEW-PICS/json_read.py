import json

# Opening JSON file
f = open('annotations.json' )

# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json
# list
for i in data["annotations"] :
    if i["image_id"] == 5:
        # print(i)
        val = i["bbox"]
        val[2]+=val[0]
        val[3]+= val[1]
        print(val,",")

# Closing file
f.close()