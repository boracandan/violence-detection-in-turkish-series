from src.database.violence_detection_database import ViolenceDetectionDatabase

def evaluate_accuracy(tableName, VDdb):
    # Get the data 
    data = VDdb.select_all(tableName, "llm_violence_prediction IS NOT ? AND violence IS NOT ?", (None, None))

    correctPredictions = 0

    for instance in data:
        # Extract the important values
        llmPrediction = instance[4]
        actualValue = instance[3]
        
        if llmPrediction == actualValue:
            correctPredictions += 1
    
    accuracy = correctPredictions / len(data) * 100
    return accuracy


if __name__ == "__main__":
    with ViolenceDetectionDatabase() as VDdb:
        accuracy = evaluate_accuracy("YalıÇapkını", VDdb)
    print(f"The model's accuracy was {accuracy}%")
