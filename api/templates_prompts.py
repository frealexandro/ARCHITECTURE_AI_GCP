

#all: class Prompts
class Prompts:

    def __init__(self):
        self.template_first_prompt_extract_description = """ Build a complete workflow in Google Cloud Platform (GCP) using only the
        command-line terminal, without any enabled APIs. You have a service account with all necessary access rights.

input:  Workflow components:
        -1.Input file:
            Name: "archivo_1.xlsx"
            Content: 82 columns of data
            Destination: GCP bucket "bucket_experiment"

        -2.GCP Bucket:
            Name: "bucket_experiment"
            Region: us-central1
            Type: Standard
            Function: Trigger for Cloud Function

        -3.Cloud Function:
            Name: "bucket_experiment"
            Region: us-central1
            Trigger: File upload to the bucket
            Functions:
                a) Verify 82 columns in the Excel file
                b) Process and export data to BigQuery

        -4.BigQuery Table:
            Name: "tabla_experiment"
            Dataset: "experiment"
            Initial state: Empty
            Update: Replaced with each new processed file

        Data flow:
            Upload of "archivo_1.xlsx" to "bucket_experiment"
            Activation of Cloud Function "bucket_experiment"
            File processing and export to BigQuery
            Replacement of data in "tabla_experiment"
            Process repetition with each new Excel file

        Instructions:
         -Provide the necessary GCP terminal commands to:
            Create the "bucket_experiment" bucket in the us-central1 region
            Upload the "archivo_1.xlsx" file to the bucket
            Create the "bucket_experiment" Cloud Function with the appropriate trigger
            Deploy the Python code for the Cloud Function that processes the file and exports to BigQuery
            Create the "experiment" dataset and "tabla_experiment" table in BigQuery
            Configure the necessary permissions for the Cloud Function to access the bucket and BigQuery

        Note: Ensure all commands are compatible with the GCP terminal and do not require additional APIs.  """

        self.template_second_prompt_extract_description = """

output:{example_input_description_architecture}


input:{input_description_architecture_context}

"""

        self.template_second_prompt = """"Analyze the following instructions and perform these tasks:

        1.Extract the number of MAIN steps from the instructions.
        2.Provide a single integer representing the total number of MAIN steps.

        Important notes:

        - Focus only on the MAIN steps, not sub-steps or minor details.
        - Ensure your answer is a single integer.
        - Do not include any explanations or additional text in your response.


input:{example_input_description_architecture}

output:{example_input_num_steps_architecture}

input:{output_description_architecture}

output:

"""

        self.template_third_prompt = """"You are an expert text analyzer with a focus on technical documentation.
        Task: Extract specific sections from the given text.
        
        I will provide you with a technical document or instructions.Extract and list the exact content from the following sections:

        1."Prerequisites"
        2."Recommendations"
        3."Possible errors"
        4."Testing"

        Instructions:

                Only include the content that explicitly appears under these exact headings.
                If a section is not present, state "No [Section Name] section found."
                Maintain the original language (Spanish or English) of the extracted content.
                Do not summarize or interpret the content; extract it verbatim.
                Use markdown formatting for better readability (e.g., ## for section headers).

input:{example_input_description_architecture}

output:{example_input_aspects_architecture}

input:{output_description_architecture}

output:

"""

        self.template_extract_step = """"You are a precise text extractor specialized in technical documentation.
        Task: Extract the exact text of a specific main step from a set of instructions.

        A set of instructions will be provided.The main step number to extract is represented by the variable {num_step}.

        The exact text of the specified main step, including its number and any substeps.
        
        Instructions:

                Identify main steps that begin with the format "**number."
                Locate the main step that matches the number provided in {num_step}.
                Extract the entire text of that step, including:

                The step number
                The main step description
                Any substeps or additional information under that main step

        Provide the extracted text verbatim, preserving all formatting, punctuation, and line breaks.
        If the specified step number doesn't exist, respond with "Step {num_step} not found in the provided instructions."

input:{output_description_architecture}

output:

"""