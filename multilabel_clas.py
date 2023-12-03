from pyabsa import AspectPolarityClassification as APC, available_checkpoints

# you can view all available checkpoints by calling available_checkpoints()
checkpoint_map = available_checkpoints(show_ckpts=True)

from pyabsa import available_checkpoints


classifier = APC.SentimentClassifier(
    checkpoint="english"
) 

examples = [
    "everything is always cooked to perfection , the [B-ASP]service[E-ASP] is excellent , the [B-ASP]decor[E-ASP] cool and understated . $LABEL$ Positive, Positive",
    "Great [B-ASP]taste[E-ASP] ever tried."
    "I think this laptop is great!",  # if you dont label an aspect, then pyabsa try to give you a 'global sentiment'. But please avoid doing that.
]

examples2 = [
    "This is a sentence. The [B-ASP]Chase Sapphire[E-ASP] card is really good. However, the [B-ASP]cashback[E-ASP] is not good.",
    "This is another sentence. The [B-ASP]Apple Card[E-ASP] card is not good."
]
for ex in examples2:
    result = classifier.predict(
        text=ex,
        print_result=True,
        ignore_error=True,  # ignore an invalid example, if it is False, invalid examples will raise Exceptions
        eval_batch_size=32,
    )
# instance inference
# result = classifier.predict(['I love this movie, it is so great!'],
#                    save_result=True,
#                    print_result=True,  # print the result
#                    ignore_error=True,  # ignore the error when the model cannot predict the input
#                    )

# inference_source = APC.APCDatasetList.Laptop14
# apc_result = classifier.batch_predict(target_file=inference_source,  #
#                                       save_result=True,
#                                       print_result=True,  # print the result
#                                       pred_sentiment=True,  # Predict the sentiment of extracted aspect terms
#                                       )

print(result)
