from api_client import (
    call_mock_sv5tot_api
)

from rules_engine import (
    evaluate_student
)

from reasoning import (
    generate_ai_reasoning
)

from database import (
    save_to_database
)


# MAIN PIPELINE
def process_student():

    # MOCK API
    extracted_json = (
        call_mock_sv5tot_api()
    )

    # RULE ENGINE
    evaluation_result = (
        evaluate_student(
            extracted_json
        )
    )

    # AI REASONING
    reasoning = (
        generate_ai_reasoning(

            extracted_json,

            evaluation_result
        )
    )

    # FINAL RESULT
    final_result = {
        "student_data":
        extracted_json,
        "evaluation":
        evaluation_result,
        "reasoning":
        reasoning
    }

    # SAVE DATABASE
    save_to_database(
        final_result
    )

    return final_result


if __name__ == "__main__":

    result = process_student()
    print(result)