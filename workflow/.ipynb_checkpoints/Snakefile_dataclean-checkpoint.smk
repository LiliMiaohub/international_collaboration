##############################################################
#contains rules that cleaning the raw data
#
#
#
#
##############################################################

rule clean_pub:
    input:
        PUB_RAW
    output:
        PUB_CLEANED,
        OSTBK2UID
    shell:
        "python scripts/clean_raw_article.py {input} {output}"
        
rule clean_raw_article_cntry:
    input:
        PUB_AUTHOR_RAW,
        AUTHOR_INFO_RAW,
        CNTRY_META
    output:
        PUB_AUTHOR_CLEANED
    shell:
        "python scripts/clean_raw_article_cntry.py {input} {output}"
        
rule clean_author_info:
    input:
        AUTHOR_INFO_RAW
    output:
        AUTHOR_INFO_CLEANED
    shell:
        "python scripts/clean_raw_author_info.py {input} {output}"
        
rule select_intl_alpha:
    input:
        PUB_AUTHOR_CLEANED,
        PUB_CLEANED
    output:
        PUB_AUTHOR_ALL,
        PUB_AUTHOR_INTL,
        PUB_AUTHOR_INTL_NOALPHA
    shell:
        "python scripts/select_intl_alpha.py {input} {output}"