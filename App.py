import requests
import os
import sys

def remove_nonpicture_files(arr, file, extensions):
    for extension in extensions:
        if file.endswith("." + extension):
            return
    arr.remove(file)
    return

print("Running " + sys.argv[0] + " with " + str(len(sys.argv)) + " args...")
if not(len(sys.argv) == 4):
    print("Please provide the paths to the two folders holding the images, and an api key when you run this program (for example: python " + sys.argv[0] + " \"C:\\Devel\\random\\ImageMapper\\items_x128\\items\\\" \"C:\\\\Devel\\random\\ImageMapper\\items\\items\" \"8f48c3c5-812a-0902-c271-9f3518b76c7b\" )")
    sys.exit(1)
print("This is the name of the script:", sys.argv[0])
print("Number of arguments:", len(sys.argv))
print("The arguments are:" , str(sys.argv))
api = r'https://api.deepai.org/api/image-similarity'
F1 = sys.argv[1]
if not(F1[len(F1)-1] == '\\' or F1[len(F1)-1] == '/'):
    F1 = F1 + "\\"
F2 = sys.argv[2]
if not(F2[len(F2)-1] == '\\' or F2[len(F2)-1] == '/'):
    F2 = F2 + "\\"
api_key = sys.argv[3]
query_count = 0
empty_count = 0
f1arr = sorted(os.listdir(F1))
f2arr = sorted(os.listdir(F2))
valid_extensions = ["png", "jpg"]
print(f"original length: {len(f1arr)} * {len(f2arr)} = {len(f1arr)*len(f2arr)}")
for file in f1arr:
    remove_nonpicture_files(f1arr, file, valid_extensions)
for file in f2arr:
    remove_nonpicture_files(f2arr, file, valid_extensions)
for f1 in f1arr:
    for f2 in f2arr:
        if f1 == f2:
            f1arr.remove(f1)
            #f2arr.remove(f2) # TODO: make flag that enables this
print(f"reduced to: {len(f1arr)} * {len(f2arr)} = {len(f1arr)*len(f2arr)}")
map = dict({r"C:/path/to/example1/.png": (r"C:\path\to\example2", 100)})
for f1 in f1arr:
    for f2 in f2arr:
        r = requests.post(
            api,
            files={
            'image1': open(F1 + f1, 'rb'),
            'image2': open(F2 + f2, 'rb'),
            },
            headers={'Api-Key': api_key}
            )
        query_count += 1
        if r.json() == None:
            print("OUTPUT WAS EMPTY")
            empty_count += 1
        elif r.json().get('output') == None:
            print(f1 + " + " + f2 + " -> None")
            continue
        val = r.json().get('output').get('distance')
        print(f1 + " + " + f2 + " -> " + str(val))
        if not(f1 in map) or val < map[f1][1]:
            map[f1] = (f2, val)
del map['C:/path/to/example1/.png']
print(map)
with open(r".\map.txt", 'w') as output_file:
    print(map, file=output_file)
print("map.txt successfully saved to the current folder.")
print("successfully finished running " + sys.argv[0] + f" with {empty_count} empty queries out of {query_count} total queries.")
