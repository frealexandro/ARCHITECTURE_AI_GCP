
#all: first function to create the pipeline description considering that the service account is already logged in the environment
from google.oauth2 import service_account
import re

#all: import the CloudStorageManager class
from cloud_storage import CloudStorageManager

#all: import the GeminiOperations class
from gemini_operations import GeminiOperations

#all: import the PromptTemplate class
from templates_prompts import Prompts
from cloud_storage import CloudStorageManager
from gemini_operations import GeminiOperations



class  Createcode:

    def __init__(self):
        
        self.example_input_description_architecture = '/home/frealexandro/proyectos_personales/gemini_pro_competition/api/examples/general_flow/example_input_description_architecture.txt'

        self.output_description_architecture = '/home/frealexandro/proyectos_personales/gemini_pro_competition/api/final_output/output_description_architecture.txt'

        self.example_input_num_steps_architecture = '/home/frealexandro/proyectos_personales/gemini_pro_competition/api/examples/general_flow/example_input_num_steps_architecture.txt'

        self.output_num_steps_architecture   = '/home/frealexandro/proyectos_personales/gemini_pro_competition/api/final_output/output_num_steps_architecture.txt'

        self.example_input_other_aspects_architecture = '/home/frealexandro/proyectos_personales/gemini_pro_competition/api/examples/general_flow/example_input_other_aspects_architecture.txt'

        self.output_other_aspects_architecture = '/home/frealexandro/proyectos_personales/gemini_pro_competition/api/final_output/output_other_aspects_architecture.txt'

    def create_code (self,path_image,prompt_user):

        #!################################################################
        #! Upload the image of the initial architecture to a Google Cloud Storage bucket

        # all: Create an object of the CloudStorageManager class
        cloud_storage_manager = CloudStorageManager()


        #*route of the image of the initial architecture deprecated
        #*/home/frealexandro/proyectos_personales/gemini_pro_competition/api/images_architectures/initial_architecture.png

        # all: use the upload_blob method to upload a file to a bucket
        cloud_storage_manager.upload_blob("gemini_pro", path_image , 'initial_architecture.png' )

        #!################################################################
        #!inicio del proceso de generacion de la descripcion de la arquitectura inicial

        # all: create language model variable
        model = "gemini-1.5-pro-001"

        # all: Create an object of the GeminiOperations class
        gemini_operations = GeminiOperations(model)

        # all: Create an object of the PromptTemplate class
        prompt_template = Prompts()

    
        #all : read description of the example architecture 
        with open( self.example_input_description_architecture , 'r') as f:
            exmaple_input_architecture = f.read()


        #all: assignment of variables to the prompt for the architecture description
        template_second_prompt_extract_description = prompt_template.template_second_prompt_extract_description.format(
            example_input_description_architecture = exmaple_input_architecture, input_description_architecture_context = prompt_user)

    
        #! A description of the flow can be added so that the Gemini model has a better interpretation.
        #all: function to generate the description of the image of the initial architecture with Gemini
        output_description_architecture = gemini_operations.generate_description_image (prompt_template.template_first_prompt_extract_description ,
                                                                                        template_second_prompt_extract_description ,
                                                                                        'initial_architecture.png' )

        #all : save the description of the output architecture
        with open( self.output_description_architecture , 'w') as f:
            f.write(output_description_architecture)

        print("The first prompt was generated correctly")

    
        #!###################################################################
        #!start of the second prompt to count the steps of the architecture

        #all: read the example of the number of steps in the example architecture
        with open(self.example_input_num_steps_architecture , 'r') as f:
            example_input_steps_architecture = f.read()


        #all: assignment of variables to the prompt to count the steps of the architecture

        template_second_prompt = prompt_template.template_second_prompt.format(
                    output_description_architecture = output_description_architecture,
                    example_input_description_architecture = exmaple_input_architecture,
                    example_input_num_steps_architecture = example_input_steps_architecture
                )

        #all: calls the step counting function with gemini
        steps_new_flow = gemini_operations.generate_count_steps(template_second_prompt)

    
        #all: save the output steps file
        with open(self.output_num_steps_architecture , 'w') as f:
            f.write(steps_new_flow)

    
    
        #all: extract the number of steps with a regex function
        number_steps = re.findall(r'\d+', steps_new_flow)
        print(f"The number of flow steps are: {number_steps[0]}")

    
        print("The second prompt was generated correctly")

        #!###################################################################
        #!start the third prompt to get other aspects of the architecture in a file

        #all: read the example of other aspects of architecture
        with open(self.example_input_other_aspects_architecture, 'r') as f:
            example_input_aspects_architecture = f.read()

        #all: assignment of variables to the prompt to obtain other aspects of the architecture
        template_third_prompt = prompt_template.template_third_prompt.format(
            example_input_description_architecture = exmaple_input_architecture,
            example_input_aspects_architecture = example_input_aspects_architecture,
            output_description_architecture = output_description_architecture
        )


    
        #all: calls the function of other aspects of the architecture, this in order to obtain other aspects of the architecture
        other_aspects = gemini_operations.get_aspects(template_third_prompt)

        #all: save file from other aspects of the architecture
        with open(self.output_other_aspects_architecture , 'w') as f:
            f.write(other_aspects)

        print("The third prompt was generated correctly")

        #!######################################################################
        #!start of the fourth prompt to extract the exact step of the instructions

    
        #all: use the variable number_steps[0] for the number of steps in the architecture flow with a for loop from 1 to the number of steps
        for i in range(int(number_steps[0])):
        
        
        #*this option is deprecated because the option to add examples does not seem useful, it may have errors since the example number varies
        # with open(f'/home/frealexandro/projects/Notebooks_2024/GEN_GCP_AI/competition_gemini_pro/examples/paso_{i+1}/paso_{i+1}.txt', 'r') as f:
        #     example_input_paso_architecture = f.read()

        
            #all: assignment of variables to the prompt to extract the exact step of the instructions
            template_extract_step = prompt_template.template_extract_step.format(
                output_description_architecture = output_description_architecture,
                num_step = i+1
            )
        
            #all: calls the function to extract the exact step of the instructions
            step = gemini_operations.extract_step(template_extract_step)


        
            #all: save the file of the extracted steps
            with open(f'/home/frealexandro/proyectos_personales/gemini_pro_competition/api/final_output/step_{i+1}.txt', 'w') as f:
                f.write(step)

            print(f"The flow step number {i+1} was extracted correctly")


            print("The fourth prompt was generated correctly")


        #!######################################################################
        #!extract the code blocks of the extracted steps
    

        for i in range(int(number_steps[0])):


            #all: read a text file with the extracted steps       
            with open(f'/home/frealexandro/proyectos_personales/gemini_pro_competition/api/final_output/step_{i+1}.txt', 'r') as f:
                step = f.read()


            #all: Extract the text into a single list with the bash, python and txt tags in the correct order of steps 
            pattern = re.compile(r'```(bash|python|txt)(.*?)```', re.DOTALL)

            #all: Add a initial small string that shows if the code block extracted is a bash, python or txt code block
            matches = pattern.findall(step)
            code_blocks = []
            for match in matches:
                block_type = match[0]  #! This will be 'bash', 'python', or 'txt'
                code_content = match[1].strip()
                code_blocks.append(f"[{block_type}]\n{code_content}")
    
            #all: Save list to a text file
            with open(f'/home/frealexandro/proyectos_personales/gemini_pro_competition/api/final_output/code_blocks_{i+1}.txt', 'w') as f:
                for block in code_blocks:
                    f.write(block + "\n\n")  #! Add two newlines for separation between blocks

            print(f"The code blocks {i+1} were extracted correctly")

        return 'the process was completed correctly'


