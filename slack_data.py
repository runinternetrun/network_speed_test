def get_url():
   #This url need to be updated with the url pointing to the slack channel where
   #the message should be sent.
   url = "not_set"
   if url == "not_set":
      print("A slack url has not been configured in slack_data.py - refer to incoming webhooks app for slack to obtain")
      exit()
   else:
      return url

