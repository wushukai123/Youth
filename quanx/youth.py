#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# 此脚本参考 https://github.com/Sunert/Scripts/blob/master/Task/youth.js

import traceback
import time
import re
import json
import sys
import os
from util import send, requests_session
from datetime import datetime, timezone, timedelta

# YOUTH_HEADER 为对象, 其他参数为字符串
# 选择微信提现30元，立即兑换，在请求包中找到withdraw2的请求，拷贝请求body类型 p=****** 的字符串，放入下面对应参数即可 YOUTH_WITHDRAWBODY
# 分享一篇文章，找到 put.json 的请求，拷贝请求体，放入对应参数 YOUTH_SHAREBODY
# 清除App后台，重新启动App，找到 start.json 的请求，拷贝请求体，放入对应参数 YOUTH_STARTBODY

cookies1 = {
  'YOUTH_HEADER': {"Accept-Encoding":"gzip, deflate, br","Cookie":"sensorsdata2019jssdkcross=%7B%22distinct_id%22%3A%2254139898%22%2C%22%24device_id%22%3A%22177dee53474413-05c33da18a2cb8-754c1251-181760-177dee534758a2%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22177dee53474413-05c33da18a2cb8-754c1251-181760-177dee534758a2%22%7D; Hm_lvt_268f0a31fc0d047e5253dd69ad3a4775=1613215270,1613295645,1613387503,1614740073; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2252335096%22%2C%22%24device_id%22%3A%22177e3a112a3af-0763f017283aef-754c1251-181760-177e3a112a4566%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22177e3a112a3af-0763f017283aef-754c1251-181760-177e3a112a4566%22%7D","Connection":"keep-alive","Content-Type":"","Accept":"*/*","Host":"kd.youth.cn","User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148","Referer":"https://kd.youth.cn/h5/20190301taskcenter/ios/index.html?uuid=c2dd0b574c73d3f1b4044ed9068e1a1c&sign=aaa3f3b3a3228796f8f108fee1867f93&channel_code=80000000&uid=54139898&channel=80000000&access=WIfI&app_version=2.0.2&device_platform=iphone&cookie_id=1e1b820273b9ec360684a1d358b1e334&openudid=c2dd0b574c73d3f1b4044ed9068e1a1c&device_type=1&device_brand=iphone&sm_device_id=202012201730083d8fc693adfc284df89a1197db3c518801059f99defc1405&device_id=49112670&version_code=202&os_version=14.5&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOxp3mzhoycm7CoqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonqWr9-2q4GviWqEY2Ft&device_model=iPhone_5&subv=1.5.1&&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOxp3mzhoycm7CoqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonqWr9-2q4GviWqEY2Ft&cookie_id=1e1b820273b9ec360684a1d358b1e334","Accept-Language":"zh-cn","X-Requested-With":"XMLHttpRequest"},
  'YOUTH_READBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjab0hHSxXenkWHSkCwB26b0x_gtnWSAWxe4W5DsfKJWZOXtKDsKYq12be0LrvmAL6NblqT9UtxAEHm7OtZxLar7-_xSSlyq6ncVwYlJemSGGgCtpKsmLSwZlYWx7-UBTNCb5cFAEHYXsate1-UMCB0PQiY4VtpFhviXfhV12qQcG2Rps4ItXcHWM7nGjqXx5QMnpLeLYWAWnx1XWKvJbDq3t5BYxwTD3IwSdyIyZddb46gpWUby4w3aJkHHKy2A4FehtI170mZVKIY57V98V5YKS3_nmvc3oDq_FvHWgLpytrC6O3pVhMVgtoqBM9kIPleIS2YH_etGhJiRtoGSjRvAa3Zz-6EmWuH1D1HU_pGk5rcmP1mwurqw2jO0bg9woLX47zdOGHYTQtHohv83SfXT3h3KnATyv4Wbg_mTdP965lNg8ovZNMX_ftl4I6A87U950JnfVD76A1NqV6gxJ5CLouEJao18XnAp5to3A3wNjLAuJeLdzZdnXvxK4fy9x7TnrMFsFJJeVrIspshxkE2Jua9TMbDOA8YK6cdEa-_S9eLKNv3_4QdcoiUdahzxq7jtAaX8nCawkycvKOJQoy_m756AwfXGDsJnilJA7MSmKKXFLLuCrYvPWpkfRwhgQk65xbM02JZ0_i_2wCIZDdi_s5nugW3EhPr0ZwBfLpKcGxnZVZAShzBLGPSk4wIM2E3rDuddLVNpjFJgouPXDoTUoI3yz-KIKbpIAIx4UsHu4Z4qzTxBFB-AJj7XgPDRlwQrJJF9bhiVxnNTsjv6xzgZ05b3J0bHF5cmRkPdjok00k7AaAheiiv_vFFWBApeDPKzVWJSh8Dnlf30ToGbhPgQTUBtxqvvBvFm41KNnNddRg%3D%3D',
  'YOUTH_READTIMEBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_mEtDEGsOrBruuZzIpWlevTEf2n4e6SDtwtHI8jh7tGLFm1iscPtbZwlhO1--2rPMqEVay5SHQZ0Xa5om9y_QnFioIoDSg-ArtrfwznZt1IhRAOspLNm4F1Z4mRILDUTDM9AS-u45jBCcm2GMY5HbKWpauyaSBxOPE6B4aEeFKW1W8MMxqHORaH1p5G4qLj7bbpDEuutDkpVsqfekqTRxJyPkQgE4ejXGhg4NAc4cDrs57ZLqKRuEu69Z9OaOA9zN-9HGKYsZ_lGFmwKljM6HhLGGEzqSKKnogw5RUnZBfIlPSEZVRR6HskgyEgNxWOZayF1rGfJPY7ADOK4ejIn59k7RCgPoN-PTtVhlIS5VGViKDRZ4X49MMU0sBMbFfK1oy3-OBD18nBbzzr8dcjO8DHaFCVI87g2-eCl9cFDS1F6oEpiDuTwieiwBFRIrHEISkR1dh0CH-UOqs-N0g9x6ebT9w2Qe5XuHriKebsPGRxE2cfBbmxezGjvXNeEvseA0UxakDD2xAysKVlK6acmjnix06LpRahjXcry_1jM9BD_hxUwY8sxSTN2TBIhe0NlaCjWSof45fgpvWA2-2jm068YDPh-5B_NH5SGd6Fe_I6gzF3WHVLC3hEKFOiaxvBI4q6sMlWlPDf5XnbQIvH7BYWofn8UdM3Gu0BHC_4ZrsP-2epFxlvt3hue9D70ynyd7vaqaZ9Bfm4z5cC8uaAL-X9ABYirnaN418futzbHpkT_wBpgED0qCGDJQHEIQvIvh35zVWx3SFGfkIf9JA9UEDfGe3wPWslHYkRRPJNGhdeo%3D',
  'YOUTH_WITHDRAWBODY': '',
  'YOUTH_SHAREBODY': 'access=WIFI&app_version=2.0.2&article_id=36485936&channel=80000000&channel_code=80000000&cid=80000000&client_version=2.0.2&device_brand=iphone&device_id=49112670&device_model=iPhone&device_platform=iphone&device_type=iphone&from=0&is_hot=0&isnew=1&mobile_type=2&net_type=1&openudid=c2dd0b574c73d3f1b4044ed9068e1a1c&os_version=14.5&phone_code=c2dd0b574c73d3f1b4044ed9068e1a1c&phone_network=WIFI&platform=3&request_time=1614762112&resolution=640x1136&sign=deac7616484c024f35d230e44057b287&sm_device_id=202012201730083d8fc693adfc284df89a1197db3c518801059f99defc1405&stype=WEIXIN&szlm_ddid=D22OXvOWHpYdQjDf%2ByB9UhXgBqQ9C%2BbV8FECXmh7wlq7AX40&time=1614762112&uid=54139898&uuid=c2dd0b574c73d3f1b4044ed9068e1a1c',
  'YOUTH_STARTBODY': 'access=WIFI&app_version=2.0.2&channel=80000000&channel_code=80000000&cid=80000000&client_version=2.0.2&device_brand=iphone&device_id=49112670&device_model=iPhone&device_platform=iphone&device_type=iphone&isnew=1&mobile_type=2&net_type=1&openudid=c2dd0b574c73d3f1b4044ed9068e1a1c&os_version=14.5&phone_code=c2dd0b574c73d3f1b4044ed9068e1a1c&phone_network=WIFI&platform=3&request_time=1614761899&resolution=640x1136&sm_device_id=202012201730083d8fc693adfc284df89a1197db3c518801059f99defc1405&szlm_ddid=D22OXvOWHpYdQjDf%2ByB9UhXgBqQ9C%2BbV8FECXmh7wlq7AX40&time=1614761899&token=854694e9ca5fc32d52f88e28fc1c0b4c&uid=54139898&uuid=c2dd0b574c73d3f1b4044ed9068e1a1c'
}
cookies2 = {
  'YOUTH_HEADER': {"Accept-Encoding":"gzip, deflate, br","Cookie":"sensorsdata2019jssdkcross=%7B%22distinct_id%22%3A%2254134778%22%2C%22%24device_id%22%3A%22177f611da7b13b-010913c159ff618-754c1251-370944-177f611da7c50a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22177f611da7b13b-010913c159ff618-754c1251-370944-177f611da7c50a%22%7D; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2254134778%22%2C%22%24device_id%22%3A%22177f634d4957f0-0e17693a0b45548-754c1251-370944-177f634d496f49%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22177f634d4957f0-0e17693a0b45548-754c1251-370944-177f634d496f49%22%7D; sajssdk_2019_cross_new_user=1","Connection":"keep-alive","Content-Type":"","Accept":"*/*","Host":"kd.youth.cn","User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148","Referer":"https://kd.youth.cn/h5/20190301taskcenter/ios/index.html?uuid=ca9f93ac64b5608d99222785ea97e2dd&sign=1dec01000ebe15954d840da86b89c297&channel_code=80000000&uid=54134778&channel=80000000&access=WIfI&app_version=2.0.2&device_platform=iphone&cookie_id=9a2cec70079894a24f02b69d15bad141&openudid=ca9f93ac64b5608d99222785ea97e2dd&device_type=1&device_brand=iphone&sm_device_id=20191116135724429da2e9b2851233e82871c56a5acecd0104dcf84979e827&device_id=48617400&version_code=202&os_version=14.5&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOxp3mzhXyYmbCoqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonqWr9-yZIOJl2qEY2Ft&device_model=iPhone_6_Plus&subv=1.5.1&&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOxp3mzhXyYmbCoqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonqWr9-yZIOJl2qEY2Ft&cookie_id=9a2cec70079894a24f02b69d15bad141","Accept-Language":"zh-cn","X-Requested-With":"XMLHttpRequest"},
  'YOUTH_READBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjab0hHSxXenkWHSkCwB26b0x_gtnWSAWxe4W5DsfKJWZGQ9DdkHA3HLdmhhuQtb3sJsiCZEv94QEphF0poWP96uCE8lRVTrRFq-TmfsjjE82oouI_KJA8SVZ77wzEp1hyoCwBTv28SavJmFDBr_K3Zuzc37JvmaIofAP4t5cKZd0VSAfloA1vY8CQ9USWiZjuGkhXqUleIr2D1ezKVqHFGYJUuNx7ibfwydgZ-KSr6VsnP69ae4ddrduwc5pnbxFj_70gPCPK1w01KBAtY1XVHz0KaxqTXjTR5txRADOvKMqypBnt68lmT2QbYsg0fhZibzexI0hWr3vBCJHP29LptRvHZHc5IKQtr4OXzsnAgLcTKXhBfj2QxTyw11KJFmJgpCZbUmvbb48Bah8SeIuiTNHA8Vd2U8FvVKcM1CQcf3mfxsHNe5-u5yz4hIe9Rx6sbzSEIgJbuGc5GmkdzLkGSI9Ln-ka8-UVBo2fk9igELznqaya4Jl-7o1Tk4UcCPwDKzU1q-PGYxNu6Tdd9HaA2Or11x8m7osOOWuriYCSML-Vl0jLuo3sLLPPb8xvE8vqQ1SDKUHA-w72U2DIUGepROMDeAjwHyHhEDgafBRlmJI-xKWTqcJhYxUghMHJUVmrZDl0KzeRQgPAF2D1Yt5kW7R7NfnljhfYG70j9aSo7V6smsyklydIkcDfRZdm8ZSHczv3-1f8A1IenCTfm6Ebh4XNcrshJWcroElc-sLT4csOboW8d2Y4YoZpSi854diaqfZWkECRpsu0WugWLpcEN8Xetgco0PISeFzrhR_JgPvG4Ylv7Vt4b1FNs7hcmdehqtrByKYd4JhCXYET8lry0M-me6bNBtMlCgd0Cg-kXWGlJ_U0Z80pf6',
  'YOUTH_READTIMEBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_mEtDEGsOrBruuZzIpWlevTEf2n4e6SDtwtHI8jh7tGLFm1iscPtbZwlhO1--2rPMqEVay5SHQZ0Xa5om9y_QnFioIoDSg-ArtrfwznZt1IhRAOspLNm4F1Z4mRILDUTDM9AS-u45jBC1EqDI9q5F1Jh8MCwGylPxtKQKCmdSZlBqvH7jmY6lCY0Fo59xHwiH75yDrFrlPIBd_l9EcCuX14T-3eD_MAsv-OxBA3kJe69_eX7dFd8FBTpOCr3xa8UHIe5EvSyE18wUXSfc65vCiNS839xZyDzxLF1czbXztmq1rMDW4DgLNohGyAMEtwfSLCcBJNG6BLiCZViu4ZMvjY-YTdxHtIlmRBE4149rqLJHRQF2JZFJAMU8RmrncwrY-IWyJeem7AgD0_IaNe6nyz6WMjWvjJrZbZtb6v1z3F2IAiZzXzHO7gd4nEoWbp7wAGvr0aVptYH2Pw45vQXioABsZrTGzFfFmLbYZTJhqslq38R9hp9cmbT7O4yELnhuIxW7sqcxJil-deKiA8wAvs1vRZ__4ZqlSA7SCqev7vhNl2C44s-4TMrc0iPrLdYl-dhUrcTrR_anZ5Ibqz0H3rDjmNXnvAfxe5cXR1_iTJEmofMWwTC0Vm4_ht3baDXJWJ7gqwYa1CBw-27aSXMyDnizJGtehYAvFLdghRWHulFmWjozKBV535kGGqqZ38oB1O8TX_f_XZ7wrtGYU1rbGpL5nkkd-oyeHaTzTzYi99RSHRlzfxweH0TUtf3w5lbEopRtCw2AYp7laA4yV7_Cu-7EXEOBVPxEouMOpquXQb0%3D',
  'YOUTH_WITHDRAWBODY': '',
  'YOUTH_SHAREBODY': 'access=WIFI&app_version=2.0.2&article_id=36370989&channel=80000000&channel_code=80000000&cid=80000000&client_version=2.0.2&device_brand=iphone&device_id=48617400&device_model=iPhone&device_platform=iphone&device_type=iphone&from=0&is_hot=0&isnew=1&mobile_type=2&net_type=1&openudid=ca9f93ac64b5608d99222785ea97e2dd&os_version=14.5&phone_code=ca9f93ac64b5608d99222785ea97e2dd&phone_network=WIFI&platform=3&request_time=1614768466&resolution=828x1792&sign=f08cf5b8b25e0a6f069bd07f393ea396&sm_device_id=20191116135724429da2e9b2851233e82871c56a5acecd0104dcf84979e827&stype=WEIXIN&szlm_ddid=D2hZQlZMFhWqaNBJSUxvTa8369TzYPJLC2t6UZzFTN47wX58&time=1614768467&uid=54134778&uuid=ca9f93ac64b5608d99222785ea97e2dd',
  'YOUTH_STARTBODY': 'access=WIFI&app_version=2.0.2&channel=80000000&channel_code=80000000&cid=80000000&client_version=2.0.2&device_brand=iphone&device_id=48617400&device_model=iPhone&device_platform=iphone&device_type=iphone&isnew=1&mobile_type=2&net_type=1&openudid=ca9f93ac64b5608d99222785ea97e2dd&os_version=14.5&phone_code=ca9f93ac64b5608d99222785ea97e2dd&phone_network=WIFI&platform=3&request_time=1614768672&resolution=828x1792&sm_device_id=20191116135724429da2e9b2851233e82871c56a5acecd0104dcf84979e827&szlm_ddid=D2hZQlZMFhWqaNBJSUxvTa8369TzYPJLC2t6UZzFTN47wX58&time=1614768673&token=0f485aa531ffad4d4ff98d8175341165&uid=54134778&uuid=ca9f93ac64b5608d99222785ea97e2dd'
}

COOKIELIST = [cookies1,2]  # 多账号准备

# ac读取环境变量
if "YOUTH_HEADER1" in os.environ:
  COOKIELIST = []
  for i in range(5):
    headerVar = f'YOUTH_HEADER{str(i+1)}'
    readBodyVar = f'YOUTH_READBODY{str(i+1)}'
    readTimeBodyVar = f'YOUTH_READTIMEBODY{str(i+1)}'
    withdrawBodyVar = f'YOUTH_WITHDRAWBODY{str(i+1)}'
    shareBodyVar = f'YOUTH_SHAREBODY{str(i+1)}'
    startBodyVar = f'YOUTH_STARTBODY{str(i+1)}'
    if headerVar in os.environ and os.environ[headerVar] and readBodyVar in os.environ and os.environ[readBodyVar] and readTimeBodyVar in os.environ and os.environ[readTimeBodyVar]:
      globals()['cookies'+str(i + 1)]["YOUTH_HEADER"] = json.loads(os.environ[headerVar])
      globals()['cookies'+str(i + 1)]["YOUTH_READBODY"] = os.environ[readBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_READTIMEBODY"] = os.environ[readTimeBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_WITHDRAWBODY"] = os.environ[withdrawBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_SHAREBODY"] = os.environ[shareBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_STARTBODY"] = os.environ[startBodyVar]
      COOKIELIST.append(globals()['cookies'+str(i + 1)])
  print(COOKIELIST)

cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)
YOUTH_HOST = "https://kd.youth.cn/WebApi/"

def get_standard_time():
  """
  获取utc时间和北京时间
  :return:
  """
  # <class 'datetime.datetime'>
  utc_datetime = datetime.utcnow().replace(tzinfo=timezone.utc)  # utc时间
  beijing_datetime = utc_datetime.astimezone(timezone(timedelta(hours=8)))  # 北京时间
  return beijing_datetime

def pretty_dict(dict):
    """
    格式化输出 json 或者 dict 格式的变量
    :param dict:
    :return:
    """
    return print(json.dumps(dict, indent=4, ensure_ascii=False))

def sign(headers):
  """
  签到
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://kd.youth.cn/TaskCenter/sign'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('签到')
    print(response)
    if response['status'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def signInfo(headers):
  """
  签到详情
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://kd.youth.cn/TaskCenter/getSign'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('签到详情')
    print(response)
    if response['status'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def punchCard(headers):
  """
  打卡报名
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}PunchCard/signUp'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('打卡报名')
    print(response)
    if response['code'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def doCard(headers):
  """
  早起打卡
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}PunchCard/doCard'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('早起打卡')
    print(response)
    if response['code'] == 1:
      shareCard(headers=headers)
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def shareCard(headers):
  """
  打卡分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  startUrl = f'{YOUTH_HOST}PunchCard/shareStart'
  endUrl = f'{YOUTH_HOST}PunchCard/shareEnd'
  try:
    response = requests_session().post(url=startUrl, headers=headers, timeout=30).json()
    print('打卡分享')
    print(response)
    if response['code'] == 1:
      time.sleep(0.3)
      responseEnd = requests_session().post(url=endUrl, headers=headers, timeout=30).json()
      if responseEnd['code'] == 1:
        return responseEnd
    else:
      return
  except:
    print(traceback.format_exc())
    return

def luckDraw(headers):
  """
  打卡分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}PunchCard/luckdraw'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('七日签到')
    print(response)
    if response['code'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def timePacket(headers):
  """
  计时红包
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}TimePacket/getReward'
  try:
    response = requests_session().post(url=url, data=f'{headers["Referer"].split("?")[1]}', headers=headers, timeout=30).json()
    print('计时红包')
    print(response)
    return
  except:
    print(traceback.format_exc())
    return

def watchWelfareVideo(headers):
  """
  观看福利视频
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}NewTaskIos/recordNum?{headers["Referer"].split("?")[1]}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print('观看福利视频')
    print(response)
    return
  except:
    print(traceback.format_exc())
    return

def shareArticle(headers, body):
  """
  分享文章
  :param headers:
  :return:
  """
  url = 'https://ios.baertt.com/v2/article/share/put.json'
  headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('分享文章')
    print(response)
    return
  except:
    print(traceback.format_exc())
    return

def threeShare(headers, action):
  """
  三餐分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}ShareNew/execExtractTask'
  headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
  body = f'{headers["Referer"].split("?")[1]}&action={action}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('三餐分享')
    print(response)
    return
  except:
    print(traceback.format_exc())
    return

def openBox(headers):
  """
  开启宝箱
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}invite/openHourRed'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('开启宝箱')
    print(response)
    if response['code'] == 1:
      share_box_res = shareBox(headers=headers)
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def shareBox(headers):
  """
  宝箱分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}invite/shareEnd'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('宝箱分享')
    print(response)
    if response['code'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def friendList(headers):
  """
  好友列表
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}ShareSignNew/getFriendActiveList'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print('好友列表')
    print(response)
    if response['error_code'] == '0':
      if len(response['data']['active_list']) > 0:
        for friend in response['data']['active_list']:
          if friend['button'] == 1:
            time.sleep(1)
            friendSign(headers=headers, uid=friend['uid'])
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def friendSign(headers, uid):
  """
  好友签到
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}ShareSignNew/sendScoreV2?friend_uid={uid}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print('好友签到')
    print(response)
    if response['error_code'] == '0':
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def sendTwentyScore(headers, action):
  """
  每日任务
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}NewTaskIos/sendTwentyScore?{headers["Referer"].split("?")[1]}&action={action}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print(f'每日任务 {action}')
    print(response)
    if response['status'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def watchAdVideo(headers):
  """
  看广告视频
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://kd.youth.cn/taskCenter/getAdVideoReward'
  headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
  try:
    response = requests_session().post(url=url, data="type=taskCenter", headers=headers, timeout=30).json()
    print('看广告视频')
    print(response)
    if response['status'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def watchGameVideo(body):
  """
  激励视频
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/Game/GameVideoReward.json'
  headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
  try:
    response = requests_session().post(url=url, headers=headers, data=body, timeout=30).json()
    print('激励视频')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def visitReward(body):
  """
  回访奖励
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/mission/msgRed.json'
  headers = {
    'User-Agent': 'KDApp/1.8.0 (iPhone; iOS 14.2; Scale/3.00)',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('回访奖励')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def articleRed(body):
  """
  惊喜红包
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/article/red_packet.json'
  headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('惊喜红包')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def readTime(body):
  """
  阅读时长
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/user/stay.json'
  headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('阅读时长')
    print(response)
    if response['error_code'] == '0':
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def rotary(headers, body):
  """
  转盘任务
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/turnRotary?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('转盘任务')
    print(response)
    return response
  except:
    print(traceback.format_exc())
    return

def rotaryChestReward(headers, body):
  """
  转盘宝箱
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/getData?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('转盘宝箱')
    print(response)
    if response['status'] == 1:
      i = 0
      while (i <= 3):
        chest = response['data']['chestOpen'][i]
        if response['data']['opened'] >= int(chest['times']) and chest['received'] != 1:
          time.sleep(1)
          runRotary(headers=headers, body=f'{body}&num={i+1}')
        i += 1
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def runRotary(headers, body):
  """
  转盘宝箱
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/chestReward?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('领取宝箱')
    print(response)
    if response['status'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def doubleRotary(headers, body):
  """
  转盘双倍
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/toTurnDouble?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('转盘双倍')
    print(response)
    if response['status'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def incomeStat(headers):
  """
  收益统计
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'https://kd.youth.cn/wap/user/balance?{headers["Referer"].split("?")[1]}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=50).json()
    print('收益统计')
    print(response)
    if response['status'] == 0:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def withdraw(body):
  """
  自动提现
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/wechat/withdraw2.json'
  headers = {
    'User-Agent': 'KDApp/1.8.0 (iPhone; iOS 14.2; Scale/3.00)',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, headers=headers, data=body, timeout=30).json()
    print('自动提现')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def bereadRed(headers):
  """
  时段红包
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}Task/receiveBereadRed'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('时段红包')
    print(response)
    if response['code'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def startApp(headers, body):
  """
  启动App
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v6/count/start.json'
  headers = {
    'User-Agent': 'KDApp/1.8.0 (iPhone; iOS 14.2; Scale/3.00)',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, headers=headers, data=body, timeout=30).json()
    print('启动App')
    print(response)
    if response['success'] == True:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def run():
  title = f'📚中青看点'
  content = ''
  result = ''
  beijing_datetime = get_standard_time()
  print(f'\n【中青看点】{beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")}')
  hour = beijing_datetime.hour
  for i, account in enumerate(COOKIELIST):
    headers = account.get('YOUTH_HEADER')
    readBody = account.get('YOUTH_READBODY')
    readTimeBody = account.get('YOUTH_READTIMEBODY')
    withdrawBody = account.get('YOUTH_WITHDRAWBODY')
    shareBody = account.get('YOUTH_SHAREBODY')
    startBody = account.get('YOUTH_STARTBODY')
    rotaryBody = f'{headers["Referer"].split("&")[15]}&{headers["Referer"].split("&")[8]}'

    if startBody:
      startApp(headers=headers, body=startBody)
    sign_res = sign(headers=headers)
    if sign_res and sign_res['status'] == 1:
      content += f'【签到结果】：成功 🎉 明日+{sign_res["nextScore"]}青豆'
    elif sign_res and sign_res['status'] == 2:
      send(title=title, content=f'【账户{i+1}】Cookie已过期，请及时重新获取')
      continue

    sign_info = signInfo(headers=headers)
    if sign_info:
      content += f'\n【账号】：{sign_info["user"]["nickname"]}'
      content += f'\n【签到】：+{sign_info["sign_score"]}青豆 已连签{sign_info["total_sign_days"]}天'
      result += f'【账号】: {sign_info["user"]["nickname"]}'
    friendList(headers=headers)
    if hour > 12:
      punch_card_res = punchCard(headers=headers)
      if punch_card_res:
        content += f'\n【打卡报名】：打卡报名{punch_card_res["msg"]} ✅'
    if hour >= 5 and hour <= 8:
      do_card_res = doCard(headers=headers)
      if do_card_res:
        content += f'\n【早起打卡】：{do_card_res["card_time"]} ✅'
    luck_draw_res = luckDraw(headers=headers)
    if luck_draw_res:
      content += f'\n【七日签到】：+{luck_draw_res["score"]}青豆'
    visit_reward_res = visitReward(body=readBody)
    if visit_reward_res:
      content += f'\n【回访奖励】：+{visit_reward_res["score"]}青豆'
    if shareBody:
      shareArticle(headers=headers, body=shareBody)
      for action in ['beread_extra_reward_one', 'beread_extra_reward_two', 'beread_extra_reward_three']:
        time.sleep(5)
        threeShare(headers=headers, action=action)
    open_box_res = openBox(headers=headers)
    if open_box_res:
      content += f'\n【开启宝箱】：+{open_box_res["score"]}青豆 下次奖励{open_box_res["time"] / 60}分钟'
    watch_ad_video_res = watchAdVideo(headers=headers)
    if watch_ad_video_res:
      content += f'\n【观看视频】：+{watch_ad_video_res["score"]}个青豆'
    watch_game_video_res = watchGameVideo(body=readBody)
    if watch_game_video_res:
      content += f'\n【激励视频】：{watch_game_video_res["score"]}个青豆'
    read_time_res = readTime(body=readTimeBody)
    if read_time_res:
      content += f'\n【阅读时长】：共计{int(read_time_res["time"]) // 60}分钟'
    if (hour >= 6 and hour <= 8) or (hour >= 11 and hour <= 13) or (hour >= 19 and hour <= 21):
      beread_red_res = bereadRed(headers=headers)
      if beread_red_res:
        content += f'\n【时段红包】：+{beread_red_res["score"]}个青豆'
    for i in range(0, 5):
      time.sleep(5)
      rotary_res = rotary(headers=headers, body=rotaryBody)
      if rotary_res:
        if rotary_res['status'] == 0:
          break
        elif rotary_res['status'] == 1:
          content += f'\n【转盘抽奖】：+{rotary_res["data"]["score"]}个青豆 剩余{rotary_res["data"]["remainTurn"]}次'
          if rotary_res['data']['doubleNum'] != 0 and rotary_res['data']['score'] > 0:
            double_rotary_res = doubleRotary(headers=headers, body=rotaryBody)
            if double_rotary_res:
              content += f'\n【转盘双倍】：+{double_rotary_res["score"]}青豆 剩余{double_rotary_res["doubleNum"]}次'

    rotaryChestReward(headers=headers, body=rotaryBody)
    for i in range(5):
      watchWelfareVideo(headers=headers)
    timePacket(headers=headers)
    for action in ['watch_article_reward', 'watch_video_reward', 'read_time_two_minutes', 'read_time_sixty_minutes', 'new_fresh_five_video_reward', 'first_share_article']:
      time.sleep(5)
      sendTwentyScore(headers=headers, action=action)
    stat_res = incomeStat(headers=headers)
    if stat_res['status'] == 0:
      for group in stat_res['history'][0]['group']:
        content += f'\n【{group["name"]}】：+{group["money"]}青豆'
      today_score = int(stat_res["user"]["today_score"])
      score = int(stat_res["user"]["score"])
      total_score = int(stat_res["user"]["total_score"])

      if score >= 300000 and withdrawBody:
        with_draw_res = withdraw(body=withdrawBody)
        if with_draw_res:
          result += f'\n【自动提现】：发起提现30元成功'
          content += f'\n【自动提现】：发起提现30元成功'
          send(title=title, content=f'【账号】: {sign_info["user"]["nickname"]} 发起提现30元成功')

      result += f'\n【今日收益】：+{"{:4.2f}".format(today_score / 10000)}'
      content += f'\n【今日收益】：+{"{:4.2f}".format(today_score / 10000)}'
      result += f'\n【账户剩余】：{"{:4.2f}".format(score / 10000)}'
      content += f'\n【账户剩余】：{"{:4.2f}".format(score / 10000)}'
      result += f'\n【历史收益】：{"{:4.2f}".format(total_score / 10000)}\n\n'
      content += f'\n【历史收益】：{"{:4.2f}".format(total_score / 10000)}\n'

  print(content)

  # 每天 23:00 发送消息推送
  if beijing_datetime.hour == 23 and beijing_datetime.minute >= 0 and beijing_datetime.minute < 10:
    send(title=title, content=result)
  elif not beijing_datetime.hour == 23:
    print('未进行消息推送，原因：没到对应的推送时间点\n')
  else:
    print('未在规定的时间范围内\n')

if __name__ == '__main__':
    run()
