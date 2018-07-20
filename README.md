mysqltoes
====
## 项目说明:
* 用于mysql数据向elasticsearch 数据迁移
* 用户mysql迁移elasticsearch 后，Elasticsearch作为mysql从，时时更新mysql数据至Elasticsearch
* 该项目可做到mysql 到 elasticsearch 热迁移同步（方法:开启maxwell，停止mysqltoes，执行logstash，开启mysqltoes）

## 项目依赖:
* CentOS 6.x
  * yum install -y gcc-c++ snappy-devel
* Python 2.7
  * pip install PyYAML
  * pip install pykafka
  * pip install python-snappy
  * pip install "elasticsearch>=6.0.0,<7.0.0"
* Java 1.8
* MySQL 5.6
* [Maxwell 1.17.1](https://github.com/zendesk/maxwell)
* [Kafka 2.11-0.9.0.1](https://archive.apache.org/dist/kafka/0.9.0.1/kafka_2.11-0.9.0.1.tgz)
* [Elasticsearch 6.3.1](https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.3.1.rpm)
* [Logstash 6.3.1](https://artifacts.elastic.co/downloads/logstash/logstash-6.3.1.rpm)

## 准备工作:
* MySQL准备
   * MySQL binlog 开启确认:<br>
        mysql>show variables like 'log_bin';<br>
        +---------------+-------+<br>
        | Variable_name | Value |<br>
        +---------------+-------+<br>
        | log_bin       | ON    |<br>
        +---------------+-------+<br>
   * MySQL binlog 格式确认:<br>
        mysql>show global variables like "binlog%";<br>
        +-----------------------------------------+--------------+<br>
        | Variable_name                           | Value        |<br>
        +-----------------------------------------+--------------+<br>
        | binlog_format                           | ROW          |<br>
        +-----------------------------------------+--------------+<br>
   * Maxwell 用户与库:<br>
        mysql> create database maxwell;<br>
        mysql> GRANT ALL on maxwell.* to 'maxwell'@'%' identified by 'xxxxxx';<br>
        mysql> GRANT SELECT, REPLICATION CLIENT, REPLICATION SLAVE on *.* to 'maxwell'@'%';<br><br>
* Kakfka安装配置
   * 根据kafka官方文档安装配置kafka集群<br><br>
* Elasticsearch安装配置
   * 根据Elasticsearch官方文档安装配置Elasticsearch集群<br><br>
* Logstash安装配置
   * 根据Logstash官方文档安装配置Logstash<br><br>
* Maxwell启动
   * wget https://github.com/zendesk/maxwell/releases/download/v1.17.1/maxwell-1.17.1.tar.gz<br>
   * tar -zxvf maxwell-1.17.1.tar.gz<br>
   * cd maxwell<br>
   * bin/maxwell --user='maxwell' --password='xxxxxx' --host='127.0.0.1' --producer=kafka --kafka.bootstrap.servers=192.168.1.1:9092,192.168.1.2:9092,192.168.1.3:9092 --kafka_topic=maxwell --kafka_version=0.9.0.1 --log_level=DEBUG<br><br>

## 项目配置说明：
    一 config目录下:<br>
      config.yaml.sample 复制为 config.yaml 并配置<br>
      db.yaml.sample 复制为 db.yaml 并配置<br>
      mapping.template.json 复制为 mapping.json<br><br>

    二 项目初始化: <br>
    ```
      # bin/mysqltoes init<br><br>
    ```

    三 导入初始数据进es:
    ```
      # cd logs/logstash/
      # /usr/share/logstash/bin/logstash -f xxx.conf
    ```
    四 数据导入成功后， 启动数据时时同步程序: 
    ```
      # bin/mysqltoes start
    ```

### db.yaml配置说明:
```php
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
```

##### 解释：
    ${database} ： 需要同步至es的 数据库名
    ${table} ： 需要同步至es的 表名
    ${es_key_field} ：声明, 同步至es后， es 的 _id字段 由 mysql的哪些字段组成, 需要注意，组成的字符串必须为全表唯一
    ${format_field} : 声明mysql中特殊格式字段，以免同步至es时出现格式错误, 目前有两种格式需要声明：
                    一 ： MySQL 中的 tinyint() 字段， 需要声明为 integer
                    二 ： MySQL 中的 所有datetime 字段， 需要声明为 datetime
    ${tracking_field} : 声明logstash jdbc中, sql_last_value 的监听字段， 一般在导出大表时，需要配置tracking_field为表自增ID或者有索引的时间字段
    ${tracking_type} ： 声明${tracking_field} 字段的类型  只支持两种： numeric timestamp
    format、jdbc_tracking 为选填项 其它为必填


