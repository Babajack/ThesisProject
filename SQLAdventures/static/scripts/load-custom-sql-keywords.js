const custom_keywords = "length sum avg round"

const sqlKeywords = " alter and as asc between by count create delete desc distinct drop from group having in insert into is join like not on or order select set table union update values where limit ";

// taken from https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.62.0/mode/sql/sql.min.js
CodeMirror.defineMIME('text/x-sqlite', {
    name: "sql",
    client: set("auth backup bail binary changes check clone databases dbinfo dump echo eqp exit explain fullschema headers help import imposter indexes iotrace limit lint load log mode nullvalue once open output print prompt quit read restore save scanstats schema separator session shell show stats system tables testcase timeout timer trace vfsinfo vfslist vfsname width"),
    keywords: set(custom_keywords + sqlKeywords + "abort action add after all analyze attach autoincrement before begin cascade case cast check collate column commit conflict constraint cross current_date current_time current_timestamp database default deferrable deferred detach each else end escape except exclusive exists explain fail for foreign full glob if ignore immediate index indexed initially inner instead intersect isnull key left limit match natural no notnull null of offset outer plan pragma primary query raise recursive references regexp reindex release rename replace restrict right rollback row savepoint temp temporary then to transaction trigger unique using vacuum view virtual when with without"),
    builtin: set("bool boolean bit blob decimal double float long longblob longtext medium mediumblob mediumint mediumtext time timestamp tinyblob tinyint tinytext text clob bigint int int2 int8 integer float double char varchar date datetime year unsigned signed numeric real"),
    atoms: set("false true null current_date current_time current_timestamp"),
    operatorChars: /^[*+\-%<>!=&|/~]/,
    dateSQL: set("date time timestamp datetime"),
    support: set("decimallessFloat zerolessFloat"),
    identifierQuote: "\"",
  });

function set(str) {
    let obj = {}, words = str.split(" ");
    for (let i = 0; i < words.length; ++i) obj[words[i]] = true;
    return obj;
  }