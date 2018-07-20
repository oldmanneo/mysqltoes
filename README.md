mysqltoes
====

# 项目依赖:
    1 CentOS 6.x  
    2 Python 2.7  
    3 MySQL 5.6  
    4 [Maxwell 1.17.1](https://github.com/zendesk/maxwell)  
    5 [Kafka 2.11-0.9.0.1](https://archive.apache.org/dist/kafka/0.9.0.1/kafka_2.11-0.9.0.1.tgz)  
    6 [Elasticsearch 6.3.1](https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.3.1.rpm)  
    
    
Python 2.7
yum install gcc-c++ snappy-devel

pip install PyYAML
pip install pykafka
pip install python-snappy
pip install "elasticsearch>=6.0.0,<7.0.0"


# 项目配置说明：
    一 config目录下:
            config.yaml.sample 复制为 config.yaml 并配置
            db.yaml.sample 复制为 db.yaml 并配置
            mapping.template.json 复制为 mapping.json

    二 项目初始化： bin/mysqltoes init

    三 导入初始数据进es
            cd logs/logstash/
            /usr/share/logstash/bin/logstash -f xxx.conf

    四 数据导入成功后， 启动数据时时同步程序: bin/mysqltoes start


#db.yaml配置说明:
${database}:
  - tablename: ${table}
    es_key:
      - ${es_key_field}
      - ${es_key_field}
    format:
      ${format_field}: integer
      ${format_field}:: datetime
    jdbc_tracking:
      column: ${tracking_field}
      type: ${tracking_type}

  - tablename: ${table}
    es_key:
      - ${es_key_field}
    format:
      ${format_field}: integer
      ${format_field}: datetime
    jdbc_tracking:
      column: ${tracking_field}
      type: ${tracking_type}

${database}:
  - tablename: ${table}
    es_key:
      - ${es_key_field}
    format:
      ${format_field}: integer
      ${format_field}:: datetime
    jdbc_tracking:
      column: ${tracking_field}
      type: ${tracking_type}

# 解释：
    ${database} ： 需要同步至es的 数据库名
    ${table} ： 需要同步至es的 表名
    ${es_key_field} ：声明, 同步至es后， es 的 _id字段 由 mysql的哪些字段组成, 需要注意，组成的字符串必须为全表唯一
    ${format_field} : 声明mysql中特殊格式字段，以免同步至es时出现格式错误, 目前有两种格式需要声明：
                    一 ： MySQL 中的 tinyint() 字段， 需要声明为 integer
                    二 ： MySQL 中的 所有datetime 字段， 需要声明为 datetime
    ${tracking_field} : 声明logstash jdbc中, sql_last_value 的监听字段， 一般在导出大表时，需要配置tracking_field为表自增ID或者有索引的时间字段
    ${tracking_type} ： 声明${tracking_field} 字段的类型  只支持两种： numeric timestamp
    format、jdbc_tracking 为选填项 其它为必填


