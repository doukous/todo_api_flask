import json
from faker import Faker
from pathlib import Path

fake = Faker()

data_list = []
data_path = Path(__file__).resolve().parent / "fake_data.json"

for person in range(5):
    fname = fake.unique.first_name()
    lname = fake.unique.last_name()
    email = fname.lower() + '@' + lname.lower() + '.com'

    data_list.append(
        {
            'username' : fname.lower(),
            'password' : 'qwerty',
            'email' : email,
            'tasks' : [fake.sentence(nb_words=5) for _ in range(4)]
        }
    )

with open(data_path, 'w', encoding='utf-8') as f:
    json.dump(data_list, f, indent=4)

if __name__ == "__main__":
    pass