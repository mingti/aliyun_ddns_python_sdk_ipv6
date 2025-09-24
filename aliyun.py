# -*- coding: utf-8 -*-
# https://api.aliyun.com/api/Alidns/2015-01-09/AddDomainRecord

from alibabacloud_tea_util.models import RuntimeOptions
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_openapi.models import Config as open_api_config
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_sts20150401.models import AssumeRoleRequest
from alibabacloud_sts20150401.client import Client as Sts20150401Client
from alibabacloud_alidns20150109.client import Client as Alidns20150109Client
from alibabacloud_alidns20150109 import models as alidns_20150109_models
from alibabacloud_credentials.models import Config as CredentialConfig
from alibabacloud_credentials.client import Client as CredentialClient
from typing import List
import os
import sys
from log import logger

from dotenv import load_dotenv
# 读取.env文件
load_dotenv()


class OpenAPI:
    def __init__(self):
        pass

    @staticmethod
    def get_STS_token() -> dict:
        """  
        使用RAM账户获取STS
        """

        res = {}
        # 从环境变量中获取RAM用户ak
        config = open_api_config(
            access_key_id=os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],
            access_key_secret=os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
        )
        config.endpoint = "sts.aliyuncs.com"
        stsClient = Sts20150401Client(config)

        # 调AssumeRole API的参数
        assume_role_request = AssumeRoleRequest(
            # 会话有效时间
            duration_seconds=3600,
            # 要扮演的RAM角色ARN，示例值：acs:ram::123456789012****:role/adminrole，可以通过环境变量ALIBABA_CLOUD_ROLE_ARN设置role_arn
            role_arn=os.environ['ALIBABA_CLOUD_ROLE_ARN'],
            # 角色会话名称，可以通过环境变量ALIBABA_CLOUD_ROLE_SESSION_NAME设置role_session_name
            role_session_name=os.environ['ALIBABA_CLOUD_ROLE_SESSION_NAME'],
        )
        runtime = RuntimeOptions()
        try:
            resp = stsClient.assume_role_with_options(
                assume_role_request, runtime)
            assumeRoleResponseBodyCredentials = resp.body.credentials

            res = {"access_key_id": assumeRoleResponseBodyCredentials.access_key_id,
                   "access_key_secret": assumeRoleResponseBodyCredentials.access_key_secret,
                   "security_token": assumeRoleResponseBodyCredentials.security_token
                   }
            logger.info("获取STS token 成功!")
            print(res)

        except Exception as error:
            # 错误 message
            logger.error("获取STS token 失败!"+str(error))

        return res

    @staticmethod
    def create_credential() -> CredentialClient:
        sts_token = OpenAPI.get_STS_token()

        # 工程代码建议使用更安全的无AK方式，凭据配置方式请参见：https://help.aliyun.com/document_detail/378659.html。
        credential = CredentialClient()
        config = CredentialConfig(
            type='sts',
            **sts_token
        )

        credential = CredentialClient(config)
        return credential

    @staticmethod
    def create_dns_client() -> Alidns20150109Client:
        """
        使用凭据初始化账号Client
        @return: Client
        @throws Exception
        """

        config = open_api_models.Config(
            credential=OpenAPI.create_credential(),
        )
        # Endpoint 请参考 https://api.aliyun.com/product/Alidns
        config.endpoint = f'alidns.aliyuncs.com'
        return Alidns20150109Client(config)

    @staticmethod
    def describe_domain_records_request(
        domain_name='dongka.top',
        rrkey_word='home.server',
        type='AAAA'
    ) -> dict:
        client = OpenAPI.create_dns_client()
        describe_domain_records_request = alidns_20150109_models.DescribeDomainRecordsRequest(
            domain_name=domain_name,
            rrkey_word=rrkey_word,
            type=type
        )
        runtime = util_models.RuntimeOptions()

        res={}
        try:
            # 复制代码运行请自行打印 API 的返回值
            resp = client.describe_domain_records_with_options(
                describe_domain_records_request, runtime)
            # resp= client.get_credential().get_type()
            res= resp.body.to_map()

        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            logger.error("请求解析记录失败"+str(error))

            # 诊断地址
            # print(error.data.get("Recommend"))
            UtilClient.assert_as_string(str(error))

        return res

    @staticmethod
    def describe_domain_records_id_and_ip(
                                domain_name: str,
                                rrkey_word: str,
                                type: str) -> dict:
        res={}
        try:
            _ = OpenAPI.describe_domain_records_request(domain_name, rrkey_word, type)

            res['record_id']=_['DomainRecords']['Record'][0]['RecordId']
            res['value']=_['DomainRecords']['Record'][0]['Value']

            logger.info("获取主机记录成功")
        except Exception as error:
            logger.error("获取主机记录失败"+str(error))
        return res
    


    @staticmethod
    def update_domain_record(
                              record_id: str,
                              rrkey_word: str,
                              type: str,
                              value: str) :

        client = OpenAPI.create_dns_client()
        update_domain_record_request = alidns_20150109_models.UpdateDomainRecordRequest(
            record_id=record_id,
            rr=rrkey_word,
            type=type,
            value=value,
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            client.update_domain_record_with_options(update_domain_record_request, runtime)
            logger.info("更新主机记录成功")

        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            logger.error("更新主机记录失败"+str(error))


if __name__ == '__main__':
    OpenAPI.get_STS_token()
