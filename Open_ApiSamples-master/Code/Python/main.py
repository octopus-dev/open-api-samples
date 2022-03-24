"""
@File    : main.py
@Software: PyCharm
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/2/23 10:52  xing       1.0          Octopus API
"""

from py_executor.scripts.open_new_api import util
base_url = 'https://openapi.bazhuayu.com/'


class Interface_Call_Credentials:
    def __init__(self):
        self.user_name = 'xxx'
        self.password = 'xxx'

    # get_new_token
    def get_new_token(self):
        token_text = self.Get_a_new_Token(base_url=base_url, username=self.user_name, password=self.password)
        return token_text

    # refresh_Token
    def The_refresh_Token(self, token):
        token_text = self.refresh_Token(base_url=base_url, refresh_token=token)
        return token_text

    @staticmethod
    def Get_a_new_Token(base_url, username, password):
        """Get the credentials for access_token

                Arguments:
                        base_url {string} -- base url of the api
                        username {String} -- The user name
                        password {String} -- password

                Returns:
                        list -- Information about token
                """
        print("Get A New Token:")
        path = 'token'
        # Post incoming parameter
        bodyData = {
            "username": username,
            "password": password,
            "grant_type": "password"
        }
        # Call interface
        response = util.request_type(host=base_url, path=path, type='post', bodyData=bodyData)
        token_info = []
        if 'error' in response.keys():
            print('ERROR_INFO:requestId: {};error code: {};error message: {}'.format(response["requestId"],
                                                                                     response['error']['code'],
                                                                                     response['error']['message']))
        else:
            token_info = response['data']
            print("Get The Token Is Successful!\n")
            print(f'Access_token: {token_info["access_token"]}')
            print(f'Access_token Validity period: {token_info["expires_in"]}')
            print(f'Token_type: {token_info["token_type"]}')
            print(f'Refresh access_token credentials: {token_info["refresh_token"]}\n')
        return token_info

    @staticmethod
    def refresh_Token(base_url, refresh_token):
        """The refresh Token

                Arguments:
                        base_url {string} -- base url of the api
                        refresh_token {string} -- Refresh access_token credentials

                Returns:
                        list -- Information about token
                """
        print("The Refresh Token:")
        path = 'token'
        # Post incoming parameter
        bodyData = {
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
        # Call interface
        response = util.request_type(host=base_url, path=path, type='post', bodyData=bodyData)
        token_info = []
        if 'error' in response.keys():
            print(
                'ERROR_INFO:error code: {};error message: {}'.format(response['error']['code'], response['error']['message']))
            print(f'requestId: {response["requestId"]}')
        else:
            token_info = response['data']
            print(("Refresh_Token Is Successful!\n"))
            print(f'New access_token: {token_info["access_token"]}')
            print(f'New Access_token Validity period: {token_info["expires_in"]}')
            print(f'New token_type: {token_info["token_type"]}')
            print(f'New Refresh access_token credentials: {token_info["refresh_token"]}\n')
        return token_info


class this_task:
    def __init__(self):
        pass

    def update_otd(self, actions, loopItems, update_text, update_url):
        for action in actions:
            # actionId
            for second_action in action["actions"]:

                # Call the function that Update the steps ,LoopAction (loopType)
                if second_action["actionType"] == "LoopType":
                    if second_action['loopType'] == 'TextList' or second_action['loopType'] == 'TEXTList':
                        # Call the interface function that update task cycle steps
                        self.update_the_contents_of_the_loop_step(token=token_str, task_id=action["taskId"],
                                                                  actionId=second_action['actionId'],
                                                                  loopType='TEXTList', loopItems=loopItems)
                    if second_action['loopType'] == 'UrlList' or second_action['loopType'] == 'URLList':
                        self.update_the_contents_of_the_loop_step(token=token_str, task_id=action["taskId"],
                                                                  actionId=second_action['actionId'],
                                                                  loopType='URLList', loopItems=loopItems)

                # Call the function that Update the steps to configure,NavigateAction and EnterTextAction
                elif second_action["actionType"] == 'EnterTextAction':
                    name = 'texttoset'
                    value = update_text
                    self.update_step_configuration(token=token_str, taskId=action["taskId"],
                                                   actionType=second_action["actionType"],
                                                   actionId=second_action['actionId'],
                                                   name=name, value=value)
                elif second_action["actionType"] == 'NavigateAction':
                    name = "url"
                    value = update_url
                    self.update_step_configuration(token=token_str, taskId=action["taskId"],
                                                   actionType=second_action["actionType"],
                                                   actionId=second_action['actionId'],
                                                   name=name, value=value)

    def get_task_group(self, token):
        groups = self.task_group(base_url=base_url, token=token)
        return groups

    def get_search_task(self, token, taskGroupId):
        tasks_info, taskid_list = self.search_task(base_url=base_url, token=token, taskGroupId=taskGroupId)
        return tasks_info, taskid_list

    def obtain_task_step_information_in_batches(self, token, taskId_list):
        actions = self.get_task_step_information(base_url=base_url, token=token, taskId_list=taskId_list)
        return actions

    def update_the_contents_of_the_loop_step(self, token, task_id, actionId, loopType, loopItems):
        self.update_loop_step(base_url=base_url, token=token, taskId=task_id, actionId=actionId, loopType=loopType,
                              loopItems=loopItems, isAppend=True)

    def update_step_configuration(self, token, taskId, actionType, actionId, name, value):
        self.update_configuration(base_url=base_url, token=token, taskId=taskId, actionType=actionType,
                                  actionId=actionId, name=name, value=value)

    @staticmethod
    def task_group(base_url, token):
        """Obtain information about all task groups of a user.
        Arguments:
                base_url {string} -- base url of the api
                token {string} -- token string from a valid token entity

        Returns:
                list -- all task groups in account
        """
        print('Get The Task Groups:')
        path = 'taskGroup'
        # Call interface
        response = util.request_type(host=base_url, path=path, type='get', tokenStr=token)
        groups = []
        if 'Error' in response.keys() or 'error' in response.keys():
            print('ERROR_INFO:error code: {};error message: {};'.format(response['error']['code'], response['error']['message']))
            print(f'RequestId: {response["requestId"]}\n')
        else:
            groups = response['data']
            print("Get The Task Groups Is Successfully!")
            for taskGroup in groups:
                print(f'TaskGroupId: {taskGroup["taskGroupId"]}')
                print(f'TaskGroupName: {taskGroup["taskGroupName"]}\n')
            print("\n")
        return groups

    @staticmethod
    def search_task(base_url, token, taskGroupId):
        """Searches for tasks in the specified task group

                Arguments:
                        base_url {string} -- base url of the api
                        token {string} -- token string from a valid token entity
                        taskGroupId {int} -- Task group ID from a valid task group

                Returns:
                        list -- All tasks in the task group
                """
        print("Search Task:")
        path = 'task/search?taskGroupId={}'.format(taskGroupId)
        # Call interface
        response = util.request_type(base_url, path, 'get', token)
        tasks_info = []
        taskid_list = []
        if 'error' in response.keys() or 'ERROR' in response.keys():
            print('ERRPR_INFO:error code: {};error message: {}'.format(response['error']['code'], response['error']['message']))
            print(f'requestId: {response["requestId"]}')
        else:
            print('Search Task Is Successful!')
            tasks_info = response['data']
            for task in tasks_info:
                print(f'TaskId: {task["taskId"]}')
                print(f'TaskName: {task["taskName"]}')
                taskid_list.append(task["taskId"])
            print('\n')
        return tasks_info, taskid_list

    @staticmethod
    def get_task_step_information(base_url, token, taskId_list):
        """Obtain step information about a batch of tasks based on step type

                Arguments:
                        base_url {string} -- base url of the api
                        token {string} -- token string from a valid token entity
                        taskId_list {String[]} -- Task Id List


                Returns:
                        list -- All step information
                """
        print("Get task step information!")
        path = 'task/getActions'

        # Post incoming parameter
        bodyData = {
            "taskIds": taskId_list,
            "actionTypes": ["LoopAction", "NavigateAction", "EnterTextAction"]
        }
        # Call interface
        response = util.request_type(host=base_url, path=path, type='post', tokenStr=token, bodyData=bodyData)
        actions = []
        if 'error' in response.keys() or 'ERROR' in response.keys():
            print(
                'ERROR_INFO:error code: {};error message: {};'.format(response['error']['code'],
                                                                      response['error']['message']))
            print(f'RequestId: {response["requestId"]}\n')
        else:
            print("Get Task Step Information Successful!")
            actions = response['data']
            for action in actions:
                for k, v in action.items():
                    print(f'{k} value: {v}')
            print("\n")
        return actions

    @staticmethod
    def update_loop_step(base_url, token, taskId, actionId, loopType, loopItems, isAppend=True):
        """Updated loop list of loop steps, now supports text list, URL list

                Arguments:
                        base_url {string} -- base url of the api
                        token {string} -- token string from a valid token entity
                        taskId {String} -- Task Id
                        actionId {String} -- The unique identifier of a step can be obtained by clicking the "Api Call Name "of
                                             the corresponding step on the client side, or through the" Batch Obtaining Task
                                             Step Information "interface
                        loopType {String} -- Circular mode, currently support: TextList(TextList), UrlList(UrlList)
                        loopItems {String[]} -- The value to be updated
                        isAppend {bool} -- Whether to append the process value, if yes, the old value is not cleared, the old
                                           value is cleared by default
                """
        print("Update Contents Of The Loop Step:")
        url = 'task/updateLoopItems'
        bodyData = {
            "taskId": taskId,
            "actionId": actionId,
            "loopType": loopType,
            "loopItems": loopItems,
            "isAppend": isAppend
        }
        response = util.request_type(host=base_url, path=url, type='post', tokenStr=token, bodyData=bodyData)
        if 'error' in response.keys():
            print(
                'ERROR_INFO:error code is {};error message is {}'.format(response['error']['code'], response['error']['message']))
            print(f'requestId: {response["requestId"]}\n')
        else:
            print("Updated loop List Of Loop Steps Is Successful!")
            print(response["data"]['message'])
            print("\n")

    @staticmethod
    def update_configuration(base_url, token, taskId, actionType, actionId, name, value):
        """Used to update the step configuration specified in the task

                Arguments:
                        base_url {string} -- base url of the api
                        token {string} -- token string from a valid token entity
                        taskId {String} -- Task Id
                        actionType {String} -- Step type: NavigateAction (open web page type), EnterTextAction
                                               (enter text type), LoopAction (loop list type)
                        actionId {String} -- The unique identifier of a step can be obtained by clicking the "Api Call
                                             Name "of the corresponding step on the client side, or through the" Batch
                                             Obtaining Task Step Information "interface
                        name {String} -- The property name
                        value {String} -- The property value
                """
        print("Update Step Configuration:")
        url = 'task/updateActionProperties'
        bodyData = {
            "taskId": taskId,
            "actions": [
                {
                    "actionType": actionType,
                    "actionId": actionId,
                    "properties": [
                        {
                            "name": name,
                            "value": value
                        }
                    ]
                }
            ]
        }
        response = util.request_type(base_url, url, 'post', token, bodyData)
        if 'error' in response.keys():
            print(
                'ERROR_INFO:error code is {};error message is {}'.format(response['error']['code'], response['error']['message']))
            print(f'requestId: {response["requestId"]}\n')
        else:
            print(response["data"]['message'])
            print("\n")


class Cloud_Collection_Related:
    def __init__(self):
        pass

    def get_Enabling_cloud_Collection(self, token, taskId):
        self.Enabling_cloud_Collection(base_url=base_url, token=token, taskId=taskId)

    def get_Stopping_cloud_Collection(self, token, taskId):
        self.Stopping_task_Collection(base_url=base_url, token=token, taskId=taskId)

    def get_Batch_obtain_task_status(self, token, taskId_list):
        task_statuss = self.Batch_obtain_task_status(base_url=base_url, token=token, taskIds=taskId_list)
        return task_statuss

    @staticmethod
    def Enabling_cloud_Collection(base_url, token, taskId):
        """Enabling cloud Collection

                Arguments:
                        base_url {string} -- base url of the api
                        token {string} -- token string from a valid token entity
                        taskId {String} -- Task Id
                """
        print("Enabling Cloud Collection:")
        path = 'cloudextraction/start'

        # Post incoming parameter
        bodyData = {
            "taskId": taskId
        }

        # Call interface
        response = util.request_type(host=base_url, path=path, type='post', tokenStr=token, bodyData=bodyData)
        if 'error' in response.keys():
            print(
                'ERROR_INFO:error code: {};error message: {}'.format(response['error']['code'], response['error']['message']))
            print(f'requestId: {response["requestId"]}\n')
        else:
            print('The {} cloud collection function is successfully started!\n'.format(taskId))

    @staticmethod
    def Stopping_task_Collection(base_url, token, taskId):
        """Stopping task Collection

                Arguments:
                        base_url {string} -- base url of the api
                        token {string} -- token string from a valid token entity
                        taskId {String} -- Task Id
                """
        print("Stopping Task Collection:")
        url = 'cloudextraction/stop'
        bodyData = {
            "taskId": taskId
        }
        response = util.request_type(base_url, url, 'post', token, bodyData)
        if 'error' in response.keys():
            print(
                'ERROR_INFO:error code is {};error message is {}'.format(response['error']['code'], response['error']['message']))
            print(f'requestId: {response["requestId"]}\n')
        else:
            print('The {} cloud collection function is successfully stopped!\n'.format(taskId))

    @staticmethod
    def Batch_obtain_task_status(base_url, token, taskIds):
        """Batch obtain task status

                Arguments:
                        base_url {string} -- base url of the api
                        token {string} -- token string from a valid token entity
                        taskIds {String[]} -- Task Id List

                Returns:
                        list -- Status of all tasks
                """
        print("Batch Obtain Task Status:")
        url = 'cloudextraction/statuses'
        bodyData = {
            "taskIds": taskIds
        }
        response = util.request_type(base_url, url, 'post', token, bodyData)
        task_statuss = []
        if 'error' in response.keys():
            print(
                'ERROR_INFO:error code is {};error message is {}'.format(response['error']['code'],
                                                                         response['error']['message']))
            print(f'requestId: {response["requestId"]}\n')
        else:
            task_statuss = response['data']
            for task_status in task_statuss:
                print(f'Task_Id is :{task_status["taskId"]}')
                print(f'Task_Name is :{task_status["taskName"]}')
                print(f'Task_Status is :{task_status["status"]}')
                print("\n")
        return task_statuss


class Data_Collection_Related:
    def __init__(self):
        pass

    def Get_unexported_data(self, token, taskId, size):
        data_list = self.unexported_data(base_url=base_url, token=token, taskId=taskId, size=size)
        return data_list

    def Marks_data_exported(self, token, taskId):
        self.Marks_the_data_as_exported(base_url=base_url, token=token, taskId=taskId)

    def get_task_all_data(self, token, taskId, offset, size):
        data_list, offset, have_data = self.task_all_data(base_url=base_url, token=token, taskId=taskId,
                                                              offset=offset, size=size)
        return data_list, offset, have_data

    def get_Clearing_Task_Data(self, token, taskId):
        self.Clearing_Task_Data(base_url=base_url, token=token, taskId=taskId)

    @staticmethod
    def unexported_data(base_url, token, taskId, size):
        """Get unexported data

        Arguments:
                base_url {string} -- base url of the api
                token {string} -- token string from a valid token entity
                taskId {String} -- task id
                size {String} -- Data article number

        Returns:
                list -- All the data

        Prompts:

        """
        print('Get Unexported Data:')
        url = f'data/notexported?taskId={taskId}&size={size}'
        response = util.request_type(base_url, url, 'get', token)
        data_list = []
        if 'error' in response.keys():
            print('ERROR_INFO:error code is {};error message is {}'.format(response['error']['code'],
                                                                           response['error']['message']))
            print(f'requestId: {response["requestId"]}\n')
        else:
            data_list = response['data']
            print(f'The total number of data: {data_list["total"]}')
            print(f'The number of exported data at now: {data_list["current"]}')
            if data_list['data']:
                print("Start output data!")
                for data in data_list['data']:
                    print(data)
                print("output data successful!\n")
            else:
                print("No Unexported Data!\n")
        return data_list

    @staticmethod
    def Marks_the_data_as_exported(base_url, token, taskId):
        """Marks the data as exported

                Arguments:
                        base_url {string} -- base url of the api
                        token {string} -- token string from a valid token entity
                        taskId {String} -- Task id
                """
        print("Marks The Data As Exported:")
        url = 'data/markexported'
        bodyData = {
            "taskId": taskId
        }
        response = util.request_type(base_url, url, 'post', token, bodyData)
        if 'error' in response.keys():
            print(
                'ERROR_INFO:error code is {};error message is {}'.format(response['error']['code'],
                                                                         response['error']['message']))
            print(f'requestId: {response["requestId"]}\n')
        else:
            print('Successfully marked the data as exported!\n')

    @staticmethod
    def task_all_data(base_url, token, taskId, offset, size):
        """Gets task data at the specified location
            When the offset is set to 0, you can get the data from the first data row and get a new offset in the response. You can use
            the offset returned to get the next batch of data rows. For example, when you set offset=0, size=100 in your first request,
            and the offset returned is offset=1024, you should use offset=1024, size=100 for the second request and get a new
            offset=1124. Then you should use offset=1124, size=100 for the third request.
            
                Arguments:
                        base_url {string} -- base url of the api
                        token {string} -- token string from a valid token entity
                        taskId {String} -- Task Id
                        offset {Number} -- Data offset. When offset is equal to 0, the task data is read from the
                                           starting position
                        size {Number} -- The value ranges from 1 to 1000

                Returns:
                        list -- All the data
                """
        print("Gets Task Data At The Specified Location:")
        url = f'data/all?taskId={taskId}&offset={offset}&size={size}'
        response = util.request_type(base_url, url, 'get', token)
        data_list = []
        have_data = True
        if 'error' in response.keys():
            print(
                'ERROR_INFO:error code is {};error message is {}'.format(response['error']['code'],
                                                                         response['error']['message']))
            print(f'requestId: {response["requestId"]}\n')
        else:
            data_list = response['data']
            print(f'The total number of data: {data_list["total"]}')
            print(f'The restTotal number of data : {data_list["restTotal"]}')
            print(f'The offset number of data : {data_list["offset"]}')
            offset = data_list['offset']
            if data_list['data']:
                print("Start output data!")
                for data in data_list['data']:
                    print(data)
                print("output data successful!\n")
            else:
                have_data = False
                print("No Data!\n")
        return data_list, offset, have_data

    @staticmethod
    def Clearing_Task_Data(base_url, token, taskId):
        """Clearing Task Data

                Arguments:
                        base_url {string} -- base url of the api
                        token {string} -- token string from a valid token entity
                        taskId {String} -- Task Id
                """
        print("Clearing Task Data:")
        url = 'data/remove'
        bodyData = {
            "taskId": taskId
        }
        response = util.request_type(base_url, url, 'post', token, bodyData)
        if 'error' in response.keys():
            print(
                'ERROR_INFO:error code is {};error message is {}'.format(response['error']['code'],
                                                                         response['error']['message']))
            print(f'requestId: {response["requestId"]}\n')
        else:
            print('The task {} data was successfully deleted. Procedure!\n'.format(taskId))


if __name__ == '__main__':
    # Instantiate class
    Interface_Call_Credentials = Interface_Call_Credentials()
    this_task = this_task()
    Cloud_Collection_Related = Cloud_Collection_Related()
    Data_Collection_Related = Data_Collection_Related()

    # Please enter an item in an account number password
    Interface_Call_Credentials.user_name = '18xxxxxxx6'
    Interface_Call_Credentials.password = 'xxxxxxx'

    # Call the function that gets the new token of the account
    token_info = Interface_Call_Credentials.get_new_token()

    # Call the function that refreshes the token interface
    # token_info = Interface_Call_Credentials.The_refresh_Token(token_info['refresh_token'])

    token_str = token_info['token_type'] + ' ' + token_info['access_token']

    # Every operation needs to obtain token_str

    # Call the function that get the task groups of the account
    # groups = this_task.get_task_group(token_str)

    # Call the function that get the task id of the account,the task_group_id from this_task.get_task_group(),str
    task_group_id = '2887296'  # e.g.
    tasks_info, taskid_list = this_task.get_search_task(token=token_str, taskGroupId=task_group_id)
    taskId_list = taskid_list

    # Call the function that get the Obtain step information about a batch of tasks based on step type,
    # the taskId_list from this_task.get_search_task(),list
    actions = this_task.obtain_task_step_information_in_batches(token=token_str, taskId_list=taskId_list)

    # Call the function that update task allocation ( as otd)
    # need to get actions , from this_task.obtain_task_step_information_in_batches(),dict
    loopItems = [  # e.g.
        'test_1',
        "test_2",
    ]
    update_text = 'test_text'  # e.g.
    update_url = 'test_url_text'  # e.g.
    this_task.update_otd(actions=actions, loopItems=loopItems,update_text=update_text,  update_url=update_url)


    taskId = '47fcxxxxxxxxxxxxxxxxxxxxxxx7a44'  # e.g.

    # Call the function that enabling cloud Collection,the taskId from this_task.get_search_task(),str
    # Cloud_Collection_Related.get_Enabling_cloud_Collection(token=token_str, taskId=taskId)

    # Call the  function that stoppping cloud Collection,the taskId from this_task.get_search_task(),str
    # Cloud_Collection_Related.get_Stopping_cloud_Collection(token=token_str, taskId=taskId)

    # Call the  function that batch obtain task status,
    # the taskId_list from this_task.get_search_task(),list
    # task_statuss = Cloud_Collection_Related.get_Batch_obtain_task_status(token=token_str, taskId_list=taskId_list)

    size = '100'  # e.g.
    # Call the  function that get task unexported data,the taskId from this_task.get_search_task(),str
    data_list = Data_Collection_Related.Get_unexported_data(token=token_str, taskId=taskId, size=size)

    # Call the  function that Marks the data as exported,the taskId from this_task.get_search_task(),str
    Data_Collection_Related.Marks_data_exported(token=token_str, taskId=taskId)

    # Call the  function that get task all data at the specified location,the taskId from this_task.get_search_task(),str
    # The offset in Start the offset,int
    offset = 0
    while True:
        asl_data_list, offset, have_data = Data_Collection_Related.get_task_all_data(token=token_str, taskId=taskId,
                                                                                     offset=offset, size=1000)
        if not have_data:
            break

    # Call the  function that Clearing Task Data,the taskId from this_task.get_search_task(),str
    # Data_Collection_Related.get_Clearing_Task_Data(token=token_str, taskId=taskId)

