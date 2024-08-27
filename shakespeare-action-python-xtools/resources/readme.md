
# APP文档帮助文档

## 一、APP介绍


描述：XTools - 编排自动化产品内置的各类小工具集合，涉及：字符串处理、类型转换、时间日期处理、加解密、编码解码等

| 内容 | 详细描述 |
| ---- | ------ |
| 上次版本      | 2.0.4 |
| 当前版本      | 2.0.5 |
| 发布时间     | 2023-10-05 21:43:53 |
| 更新时间     | 2024-08-27 10:46:00 |
| 更新人员     | [wzfukui](https://github.com/wzfukui) |
| 更新地址        | [flagify-com/OctoMationApps](https://github.com/flagify-com/OctoMationApps) |

## 二、app使用注意事项

1）RSA加密部分

- 不建议敏感系统直接使用应用动作，避免密钥泄露
- JS代码的填充方式默认是：PKCS1v15
- 通过OpenSSL生成的证书文件，可能有密码保护


2）依赖项

```
pip install cryptography
```

## APP动作清单


### str_concat（字符串_拼接多个字符串（支持拼接符））

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str1 | 第一个字符串 | string | 是 | |
| str2 | 第二个字符串 | string | 是 | |
| str3 | 第三个字符串（如有） | string | 否 | |
| str4 | 第四个字符串（如有） | string | 否 | |
| str5 | 第五个字符串（如有） | string | 否 | |
| str6 | 第六个字符串（如有） | string | 否 | |
| concat_symbol | 拼接符，默认为：空，字符串直接连接 | string | 否 | |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.str_concated | 拼接后的字符串 | string | |

### str_split（字符串_分割字符串（支持分隔符，默认为空格））

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str_to_split | 待分割的字符串 | string | 是 | |
| split_symbol | 字符串分隔符，默认为：英文逗号 | string | 否 | , |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.str_array.* | 分割后的字符串(数组循环输出） | string | |
| action_result.data.str_array | 分割后的字符串数组 | jsonArray | |

### str_splitlines（字符串_分割字符串（按行分割））

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str_to_split | 待分割的字符串 | string | 是 | |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.str_array.* | 分割后的字符串（数组循环输出） | string | |
| action_result.data.str_array | 分割后的字符串数组 | jsonArray | |

### str_replace（字符串_字符串替换）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str_original | 待处理的原始字符串 | string | 是 | |
| str_old | 字符串_替换前的字符串 | string | 是 | |
| str_new | 字符串_替换后的字符串 | string | 是 | |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.str_replaced | 替换处理后的字符串 | string | |

### str_length（字符串_计算字符串长度）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str | 字符串 | string | 是 | |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.str_length | 字符串长度 | integer | |

### str_reverse（字符串_字符串反转）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str | 待反转的字符串 | string | 是 | |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.str_reversed | 反转后的字符串 | string | |

### str_substring_with_index（字符串_截取子字符串，根据start和end位置[开始，结束)）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str_original | 待处理的原始字符串 | string | 是 | |
| start | 开始位置（会被保留） | integer | 是 | 0 |
| end | 结束位置（保留到前一位） | integer | 是 | 0 |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.str_substring | 截取后的子字符串 | string | |

### str_substring_with_start_and_length（字符串_截取子字符串，根据start和length长度）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str_original | 待处理的原始字符串 | string | 是 | |
| start | 开始位置（会被保留） | integer | 是 | 0 |
| length | 截取子字符串的长度 | integer | 是 | 0 |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.str_substring | 截取后的子字符串 | string | |

### str_to_int（字符串_转整型）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str | 字符串，默认：0 | string | 是 | 0 |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.str_int | 截取后的子字符串 | integer | |

### str_to_double（字符串_转Double型(Java)）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str | 字符串，默认：0.0 | string | 是 | 0.0 |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.str_double | 截取后的子字符串 | double | |

当然，我会继续为您列出剩余的动作。这是下一部分：

### str_to_long（字符串_转Long型(Java)）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str | 字符串，默认：0 | string | 是 | 0 |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.str_long | 截取后的子字符串 | integer | |

### str_to_bool（字符串_转布尔型）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str | 字符串（不区分大小写），默认：True，支持：true、false、<br/>yes、no、1、0、T、F、Y、N、success、failure | string | 是 | True |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.str_bool | 转换后的布尔值 | integer | |

### str_to_upper（字符串_转大写）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str | 字符串 | string | 是 | |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.str_upper | 转换后的布尔值 | integer | |

### str_to_lower（字符串_转小写）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str | 字符串 | string | 是 | |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.str_lower | 转换后的布尔值 | integer | |

### str_strip（字符串_修剪字符串首尾（空格、换行等））

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str_original | 原始字符串 | string | 是 | |
| strip_method | 修剪方式，默认：两端都修剪，支持：BOTH、LEFT、RIGHT | string | 否 | BOTH |
| strip_symbol | 修剪字符串，不填写则默认修剪空格、换行符 | string | 否 | |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.str_stripped | 修剪后的字符串 | integer | |

### str_escape（字符串_转义字符串中的特殊字符）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str_original | 原始字符串 | string | 是 | |
| escape_string_array | 需要转义的方式，默认：反斜线方式转义：反斜线、双引号 | jsonArray | 否 | ["\\", "\""] |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.str_escaped | 修剪后的字符串 | integer | |

### str_random_string（字符串_随机产生字符串）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| min_length | 字符串最小长度 | integer | 是 | 1 |
| max_length | 字符串最大长度 | integer | 是 | 10 |
| avaliable_chars | 可供随机选择的字符 | string | 否 | 1234567890<br/>abcdefghijklmnopqrstuvwxyz<br/>ABCDEFGHIJKLMNOPQRSTUVWXYZ |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.str_random | 随机字符串 | integer | |

### type_to_type（类型_通用类型转换，支持：int、long、double、str、boolean）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| input_value | 输入值，支持各种类型，默认：0 | string | 是 | 0 |
| type_to | 要转换的目标类型，支持：integer、long、double、string、boolean | string | 否 | string |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.converted_value_int | 转换后的整数型值 | integer | |
| action_result.data.converted_value_long | 转换后的长整型值 | double | |
| action_result.data.converted_value_double | 转换后的双精度型值 | long | |
| action_result.data.converted_value_string | 转换后的字符串型值 | string | |
| action_result.data.converted_value_boolean | 转换后的布尔型值 | boolean | |

### encode_base64encode（编码_Base64编码）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str | 待编码的字符串 | string | 是 | |
| encode | 字符编码，默认：UTF-8 | string | 否 | utf-8 |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.str_base64_encode | Base64编码后的字符串 | string | |


### encode_base64decode（编码_Base64解码）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str_base64 | 待解码的base64字符串 | string | 是 | |
| encode | 字符编码，默认：UTF-8 | string | 否 | utf-8 |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.str_base64_decode | Base64解码后字符串 | string | |

### encode_urlencode（编码_UrlEncode编码）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str | 待编码的字符串 | string | 是 | |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.str_url_encode | UrlEncode编码后的字符串 | string | |

### encode_urldecode（编码_UrlDecode解码）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str_url_encoded | 待解码的字符串 | string | 是 | |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.str_url_decoded | UrlDecode解码后的字符串 | string | |

### encrypt_hash（加密_哈希摘要(支持：MD5、SHA1、SHA256、SHA512等)）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str | 原始字符串 | string | 是 | |
| hash_method | 摘要算法，默认：MD5 | string | 否 | MD5 |
| encode | 字符编码方式，默认：UTF-8 | string | 否 | utf-8 |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.str_hashed | HASH摘要字符串 | string | |

### encrypt_hmac（加密_HMAC摘要(支持：MD5、SHA1、SHA256、SHA512等)）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str | 原始字符串 | string | 是 | |
| key | HMAC密钥 | password | 是 | |
| digest_method | 摘要算法，默认：MD5 | string | 否 | MD5 |
| encode | 字符编码方式，默认：UTF-8 | string | 否 | utf-8 |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.str_hmaced | HMAC摘要字符串 | string | |

### encrypt_aes_encrypt（加密_AES加密）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str | 原始字符串 | string | 是 | |
| mode | 加密方式，默认：ECB | string | 是 | ECB |
| key | 加密密钥，128，192，256位长度，对应：16，24，32个字符 | password | 是 | |
| cbc_iv | 初始化向量（仅在CBC模式下需要） ，<br/>不填写则默认为key的前16字符 | string | 否 | |
| encode | 字符编码方式，默认：UTF-8 | string | 否 | utf-8 |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.str_aes_encrypted | AES加密后字符串 | string | |

### encrypt_aes_decrypt（加密_AES解密）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str_aes_encrypted | 待解密的AES加密字符串 | string | 是 | |
| mode | 加密方式，默认：ECB | string | 是 | ECB |
| key | 加密密钥，128，192，256位长度，对应：16，24，32个字符 | password | 是 | |
| cbc_iv | 初始化向量（仅在CBC模式下需要） ，<br/>不填写则默认为key的前16字符 | string | 否 | |
| encode | 字符编码方式，默认：UTF-8 | string | 否 | utf-8 |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.str_aes_decrypted | AES解密后字符串 | string | |

### encrypt_rsa_encrypt（加密_RSA加密）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str | 原始字符串 | string | 是 | |
| public_key | RSA公钥字符串 | password | 是 | |
| padding_method | 填充模式，默认：PKCS1v15，<br/>支持：OAEP_SHA256, OAEP_SHA1, PKCS1v15 | string | 否 | PKCS1v15 |
| encoding | 字符编码方式，默认：UTF-8 | string | 否 | utf-8 |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.str_rsa_encrypted | RSA加密后字符串 | string | |


### encrypt_rsa_decrypt（加密_RSA解密）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str_rsa_encrypted | 待解密的RSA加密字符串 | string | 是 | |
| private_key | RSA私钥字符串 | password | 是 | |
| padding_method | 填充模式，默认：PKCS1v15，<br/>支持：OAEP_SHA256, OAEP_SHA1, PKCS1v15 | string | 否 | PKCS1v15 |
| private_key_has_password | Private Key是否有密码保护，默认：False | string | 否 | false |
| private_key_password | Private Key的保护密码，默认：空，<br/>与private_key_has_password组合使用 | password | 否 | |
| encoding | 字符编码方式，默认：UTF-8 | string | 否 | utf-8 |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.str_rsa_decrypted | RSA解密后字符串 | string | |

### file_info（文件_返回文件信息(根据文件路径)）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| file_path | 文件路径，如：/opt/shakespeare/test.txt，<br/>不要使用单双引号 | string | 是 | |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.file_exists | 文件是否存在 | boolean | |
| action_result.data.isdir | 是否为目录 | boolean | |
| action_result.data.isfile | 是否为文件 | boolean | |
| action_result.data.islink | 是否为链接 | boolean | |
| action_result.data.file_name | 文件名 | string | |
| action_result.data.file_realpath | 文件绝对路径 | string | |
| action_result.data.file_relativepath | 文件相对路径 | string | |
| action_result.data.file_dirname | 文件目录名 | string | |
| action_result.data.file_size | 文件大小，单位：字节 | integer | |
| action_result.data.file_ctime | 文件创建时间.时间戳 | integer | |
| action_result.data.file_ctime_str | 文件创建时间.字符串 | string | |
| action_result.data.file_mtime | 文件修改时间.时间戳 | integer | |
| action_result.data.file_mtime_str | 文件修改时间.字符串 | string | |
| action_result.data.file_atime | 文件访问时间.时间戳 | integer | |
| action_result.data.file_atime_str | 文件访问时间.字符串 | string | |
| action_result.data.file_md5sum | 文件MD5摘要 | string | |

### file_read（文件_返回文件信息(根据文件路径)）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| file_path | 文件路径，如：/opt/shakespeare/test.txt，<br/>不要使用单双引号 | string | 是 | |
| encode | 文件内容字符编码，默认：UTF-8 | string | 否 | utf-8 |
| file_size_limit | 文件大小限制，默认512KB以上文件不读取，<br/>不建议太大 | integer | 否 | 512 |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.file_content_text | 文件内容文本 | boolean | |

### math_expression（数学_表达式运算）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| expression | 数学运算表达式，支持：^[-+*/()0-9.eE%\\s]+$ | string | 是 | 1+1 |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.int_value | 数学计算结果.整数 | integer | |
| action_result.data.long_value | 数学计算结果.长整数 | long | |
| action_result.data.double_value | 数学计算结果.双精度 | double | |
| action_result.data.string_value | 数学计算结果.字符串 | string | |

### datetime_timestamp_to_timestr（日期时间_时间戳转日期时间字符串）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| timestamp | timestamp时间戳（秒），如：1616652800，<br/>不填则为当前时间 | integer | 否 | |
| format | 日期输出的格式化字符串，按需输入，<br/>如：%Y-%m-%d %H:%M:%S | string | 否 | |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.datetime_str | 日期时间字符串 | string | |
| action_result.data.datetime_timestamp | 日期时间timestamp（秒） | integer | |

### datetime_timestr_to_timestamp（日期时间_日期时间字符串转时间戳）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| timestr | 日期时间字符串，如：2021-03-10 12:00:00 | string | 是 | |
| format | 日期时间格式化字符串，按需输入，<br/>如：%Y-%m-%d %H:%M:%S | string | 是 | |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.datetime_str | 日期时间字符串 | string | |
| action_result.data.datetime_timestamp | 日期时间timestamp（秒） | integer | |

### datetime_timestamp_days_before（日期时间_根据timestamp返回N天前（后）的日期时间）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| timestamp | 日期时间戳（秒），如果为空，则为当前时间 | string | 是 | |
| days_before | N天前，或N天后，正数表示N天前，负数表示N天后 | integer | 是 | |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.datetime_str | N天前.日期时间字符串 | string | |
| action_result.data.datetime_timestamp | N天前的.日期时间timestamp（秒） | integer | |


### random_sleep

**描述**：随机Sleep，等待N秒

**入参说明**

| 参数 | 类型 | 数据样例 | 必须 | 默认值 | 说明 |
|:-----|:-----|:---------|:-----|:-----|:-----|
| min_seconds | 整数 | | 是 | 1 | 最小Sleep时间，单位：秒 |
| max_seconds | 整数 | | 是 | 10 | 最大Sleep时间，单位：秒，
超过300秒请选择异步动作 |

**出参说明**

| 参数 | 类型 | 数据样例 | 默认值 | 说明 |
|:-----|:-----|:---------|:-----|:-----|
| action_result.data.sleep_seconds | 整数 | | 1 | 随机休眠的时间（秒） |
| action_result.summary.statusCode | 整数 | | 0 | 返回错误码 |
| action_result.summary.msg | 字符串 | | | 返回消息 |

### ip_in_range（判断IP地址是否在某个段内）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| ip | 要判断的IP地址，Demo: 192.168.1.123 | string | 是 | |
| start | 起始IP地址， Demo: 192.168.1.1 | string | 是 | |
| end | 结束IP地址， Demo: 192.168.1.254 | string | 是 | |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.is_range | 如果在段内则返回真，否则返回假 | boolean | |

### search（字符串搜索）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str_data | 完整字符串 | string | 是 | |
| sub | 要搜索的字符 | string | 是 | |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.is_find | 是否搜索到 | boolean | |

### regex_match（字符串正则匹配）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| str_data | 完整字符串 | string | 是 | |
| pattern | 正则表达式 | string | 是 | |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.findall.* | 匹配到的字符串列表 | string | |

### cache_mgmt（缓存管理）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| key | 缓存的key,建议不同业务增加不同的前缀，避免key一样 | string | 是 | |
| value | 缓存的值 | string | 否 | |
| ttl | 缓存的时效, 不填则不存在失效时间，计量单位为秒 | integer | 否 | |
| operate | 缓存操作 | string | 是 | |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.key | Key | string | |
| action_result.data.value | 值 | string | |
| action_result.data.status | 操作是否成功 | boolean | |


### do_nothing

**描述**：啥也不干，你来定标题

**入参说明**

| 参数 | 类型 | 数据样例 | 必须 | 默认值 | 说明 |
|:-----|:-----|:---------|:-----|:-----|:-----|
| input | 字符串 | | 否 | | 任何输入 |

**出参说明**

| 参数 | 类型 | 数据样例 | 默认值 | 说明 |
|:-----|:-----|:---------|:-----|:-----|
| action_result.data.output | 字符串 | | | 输出 |
| action_result.summary.statusCode | 整数 | | 0 | 返回错误码 |
| action_result.summary.msg | 字符串 | | | 返回消息 |


### get_file_download_url（获取文件下载地址）

#### 入参

| 参数名 | 参数描述 | 参数类型 | 是否必填 | 默认值 |
|--------|----------|----------|----------|--------|
| file_path | 文件相对路径，/opt/shakespeare/data/app_files/action_local/<br/>下的相对路径，如：test/test.txt | string | 是 | |

#### 出参

| 参数名 | 参数描述 | 参数类型 | 备注 |
|--------|----------|----------|------|
| action_result.data.download_url | 下载地址 | string | |
| action_result.data.uuid | SDK中文件uuid | string | |


## 更新说明
- 2024-08-20 v2.0.3 优化各字符串函数，并增加AES、RSA加解密
- 2024-08-27 v2.0.4 增加随机Sleep延迟等待动作
- 2024-08-27 v2.0.5 增加一个啥也不干的空动作，输出输入