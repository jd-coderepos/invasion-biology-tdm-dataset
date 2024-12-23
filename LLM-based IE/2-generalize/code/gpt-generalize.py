from openai import OpenAI
import json
import os

# Initialize the OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    api_key = input("Please enter your OpenAI API key: ").strip()
client = OpenAI(api_key=api_key)

def collect_schemas():
    schemas = []
    print("Enter the nine schemas one by one as JSON. Press Enter three times in a row when done typing each schema:")
    for i in range(9):
        print(f"Schema {i + 1}:")
        user_input = ""
        empty_lines = 0
        while True:
            line = input()
            if line.strip() == "":
                empty_lines += 1
                if empty_lines >= 3:  # Check for three consecutive empty lines
                    break
            else:
                empty_lines = 0
                user_input += line + "\n"
        try:
            schema = json.loads(user_input)
            schemas.append(schema)
        except json.JSONDecodeError:
            print("Invalid JSON. Please re-enter the schema.")
            i -= 1  # Reattempt the current schema
    return schemas

def generate_generalized_model(schemas):
    # System prompt definition
    system_prompt = """
	**Your role**
    You are a research assistant specializing in invasion biology or ecology. You also possess an expertise in semantic modeling. Your primary task is to read and analyze various semantic models which were generated as an information extraction objective over research papers.

    The field of invasion biology is defined as follows: a research area focusing on the translocation, establishment, spread, impact, and management of species outside of their native ranges, where they are referred to as non-native or alien species.

    The semantic models are centered on the following entities: species, location, habitat, and ecosystem.
	
	The entities are defined as:
    1. **Species**: This includes both specific, formally named species (e.g., *Asterias amurensis*) and broader categories of organisms relevant to the study (e.g., "demersal fish" or "aquatic invertebrates"). These may include plants, animals, fungi, or microbes that are translocated to new environments, where they establish, spread, and potentially cause ecological or economic impacts. The term may also encompass higher-level taxonomic groups or functional groups when specific species are not identified in the text. Note generic terms like "invasive species" is not considered a species name.
    2. **Location**: The study site, which could range from a specific geographic feature (e.g., "Port Phillip Bay, southern Australia") to broader geopolitical regions (e.g., "southern Australia" or "the Amazon rainforest"). Locations may include natural features such as rivers, bays, or mountains, as well as administrative areas like cities, states, or countries.
    3. **Ecosystem**: A system comprising interacting biological and abiotic components. Ecosystems often extend beyond specific locations (e.g., the savannah ecosystem spans geopolitical boundaries such as Kenya and Tanzania).
    4. **Habitat**: A subcomponent of an ecosystem where a specific organism lives. For example, crocodiles inhabit freshwater habitats (e.g., rivers) within the broader savannah ecosystem.
	
	**Your task**
	1. Read the nine semantic models provided and come up with a generalized semantic model. The data structure to respond in is JSON.
	2. For the species the first part of the schema can look as follows:
	```
	      {
          "species": [list of species mentioned],
          "habitat": [list of habitats mentioned],
          "location": [list of locations mentioned],
          "ecosystem": [list of ecosystems mentioned]
		  }
	```
	3. Extend this semantic model with the relations by generalizing over the various relation structures modeled. Note the relation structure should not be actual relation name instances but a generic structure with properties that allow specifying a name and related entities.
	4. Note the provided input semantic models will have data instances. To come up with a generic model, you will ignore the data instances and propose the most generic model only with the properties. This semantic model will then resultingly be applied on papers to extract information from them.
	
	**Response Format:**
	1. Your response must always be in valid JSON format.
    """

    # Prepare schemas as a JSON string for the prompt
    schemas_text = json.dumps(schemas, indent=2)
    user_prompt = f"\n\nSchemas:\n{schemas_text}\n\nGenerate the generalized semantic model in valid JSON format."

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Return the assistant's response
    return response.choices[0].message.content

def main():
    print("Semantic Model Generalization Tool\n")
    schemas = collect_schemas()
    if not schemas:
        print("No schemas provided. Exiting.")
        return

    print("Generating generalized semantic model...")
    generalized_model = generate_generalized_model(schemas)

    print("\nGeneralized Semantic Model:")
    print(generalized_model)

if __name__ == "__main__":
    main()
