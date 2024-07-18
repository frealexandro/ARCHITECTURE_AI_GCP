from langchain.chains import SimpleChain
from langchain.prompts import PromptTemplate
from langchain.models import GenerativeModel
from langchain.storage import LocalStorage

#! Assuming 'credentials' is already defined in your environment.
vertexai.init(project="datalake-analytics-339922", location="us-central1", credentials=credentials)
model = GenerativeModel("gemini-1.5-pro-001")

#! Define the individual functions as chains
def generate_description_image_chain(prompt_1, prompt_2, name_image):
    try:
        route_image2 = f"gs://gemini_pro/{name_image}"
        image1 = Part.from_uri(mime_type="image/png", uri="gs://gemini_pro/ejemplo_arquitectura.png")
        image2 = Part.from_uri(mime_type="image/png", uri=route_image2)
        response = model.generate_content([prompt_1, image1, prompt_2, image2, "output:"])
        return {"output_description_architecture": response.text}
    except Exception as e:
        print(f"Error generating description for image {name_image}: {str(e)}")
        return {"output_description_architecture": ""}

def generate_count_steps_chain(prompt, output_description_architecture, example_input_description_architecture, example_input_num_steps_architecture):
    try:
        final_prompt = prompt.format(
            output_description_architecture=output_description_architecture,
            example_input_description_architecture=example_input_description_architecture,
            example_input_num_steps_architecture=example_input_num_steps_architecture
        )
        response = model.generate_content([final_prompt])
        return {"steps_new_flow": response.text}
    except Exception as e:
        print(f"Error finding the number of steps in {final_prompt}: {str(e)}")
        return {"steps_new_flow": ""}

def get_aspects_chain(prompt_aspects, output_description_architecture, example_input_description_architecture, example_input_aspects_architecture):
    try:
        final_prompt = prompt_aspects.format(
            output_description_architecture=output_description_architecture,
            example_input_description_architecture=example_input_description_architecture,
            example_input_aspects_architecture=example_input_aspects_architecture
        )
        response = model.generate_content([final_prompt])
        return {"other_aspects": response.text}
    except Exception as e:
        print(f"Error finding the number of steps in {final_prompt}: {str(e)}")
        return {"other_aspects": ""}

def extract_step_chain(prompt, output_description_architecture, num_paso):
    final_prompt = prompt.format(output_description_architecture=output_description_architecture, num_paso=num_paso)
    try:
        response = model.generate_content([final_prompt])
        return {"step": response.text}
    except Exception as e:
        print(f"Error finding the number of steps in {final_prompt}: {str(e)}")
        return {"step": ""}

#! Define the prompts templates
template_primer_prompt_extraer_descripcion = """I want to build this flow from start to finish using only GCP command-line terminal.
I don't have any enabled APIs from any GCP service. I only have a service account enabled with all the accesses.
I want the Step by Step instructions. Additionally, tell me the Prerequisites, Recommendations, Possible errors, and Testing to properly evaluate this flow.
You can use Python as the programming language to complete the logic inside any component.
If necessary, please provide the dependencies and packages for successful code execution.

input:"""

template_segundo_prompt_extraer_descripcion = """
output:{example_input_description_architecture}

input:
"""

template_segundo_prompt = """
Extract the number of MAIN steps from the following instructions and give me an integer number of how many MAIN steps there are in total:

input:{example_input_description_architecture}

output:{example_input_num_steps_architecture}

input:{output_description_architecture}

output:
"""

template_tercer_prompt = """
Please extract the following information exactly from this text ("Prerequisites", "Recommendations", "Possible errors", "Testing")

input:{example_input_description_architecture}

output:{example_input_aspects_architecture}

input:{output_description_architecture}

output:
"""

template_extraer_paso = """
Extract the information of the main step number {num_paso} from the following instructions.
I want exactly the same text, you can recognize it because all main steps start with these characters "**1."

input:{output_description_architecture}

output:
"""

#! Define the chain steps
generate_description_image_step = SimpleChain(
    input_variables=["prompt_1", "prompt_2", "name_image"],
    output_variables=["output_description_architecture"],
    chain_function=generate_description_image_chain
)

generate_count_steps_step = SimpleChain(
    input_variables=["prompt", "output_description_architecture", "example_input_description_architecture", "example_input_num_steps_architecture"],
    output_variables=["steps_new_flow"],
    chain_function=generate_count_steps_chain
)

get_aspects_step = SimpleChain(
    input_variables=["prompt_aspects", "output_description_architecture", "example_input_description_architecture", "example_input_aspects_architecture"],
    output_variables=["other_aspects"],
    chain_function=get_aspects_chain
)

#! Function to handle looping over steps
def loop_extract_steps(output_description_architecture, num_steps):
    steps = []
    for i in range(1, num_steps + 1):
        step_result = extract_step_chain(template_extraer_paso, output_description_architecture, i)
        steps.append(step_result["step"])
    return steps

#! Final chain execution
def run_chain():
    #! Initialize variables
    example_input_description_architecture = "Example architecture description"
    example_input_num_steps_architecture = "3"
    example_input_aspects_architecture = "Example architecture aspects"

    #! Generate description
    description_result = generate_description_image_step.run({
        "prompt_1": template_primer_prompt_extraer_descripcion,
        "prompt_2": template_segundo_prompt_extraer_descripcion,
        "name_image": "initial_architecture.png"
    })
    output_description_architecture = description_result["output_description_architecture"]

    #! Generate count of steps
    steps_result = generate_count_steps_step.run({
        "prompt": template_segundo_prompt,
        "output_description_architecture": output_description_architecture,
        "example_input_description_architecture": example_input_description_architecture,
        "example_input_num_steps_architecture": example_input_num_steps_architecture
    })
    steps_new_flow = steps_result["steps_new_flow"]
    num_steps = int(re.findall(r'\d+', steps_new_flow)[0])

    #! Get aspects
    aspects_result = get_aspects_step.run({
        "prompt_aspects": template_tercer_prompt,
        "output_description_architecture": output_description_architecture,
        "example_input_description_architecture": example_input_description_architecture,
        "example_input_aspects_architecture": example_input_aspects_architecture
    })
    other_aspects = aspects_result["other_aspects"]

    #! Loop to extract each step
    steps = loop_extract_steps(output_description_architecture, num_steps)
    
    return {
        "output_description_architecture": output_description_architecture,
        "steps_new_flow": steps_new_flow,
        "num_steps": num_steps,
        "other_aspects": other_aspects,
        "steps": steps
    }

#! Run the final chain
final_result = run_chain()

print(final_result)
