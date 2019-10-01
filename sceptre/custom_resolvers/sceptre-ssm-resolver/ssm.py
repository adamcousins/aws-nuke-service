# -*- coding: utf-8 -*-

import logging

from botocore.exceptions import ClientError

from sceptre.resolvers import Resolver


class SSM(Resolver):
    """
    Resolver for SSM. Resolves the value stored in the parameter store.

    :param argument: The SSM parameter
    :type argument: str

    """

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(__name__)
        super(SSM, self).__init__(*args, **kwargs)

    def resolve(self):
        """
        Retrieves the parameter value from SSM Parameter Store.

        :returns: parameter value
        :rtype: str
        """
        decoded_value = None
        if self.argument:
            param = self.argument
            connection_manager = self.stack.connection_manager
            try:
                response = connection_manager.call(
                    service="ssm",
                    command="get_parameter",
                    kwargs={"Name": param,
                            "WithDecryption": True},
                    profile=self.stack.profile,
                    region=self.stack.region,
                    stack_name=self.stack.name
                )
            except ClientError as e:
                if "ParameterNotFound" in e.response["Error"]["Code"]:
                    self.logger.error("%s - ParameterNotFound: %s",
                                      self.stack.name, param)
                raise e
            decoded_value = response['Parameter']['Value']
        return decoded_value