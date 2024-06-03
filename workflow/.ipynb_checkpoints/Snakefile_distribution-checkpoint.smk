#####################################################################
#contains rules that plot distribution in general and over authorship
#
#
#
#
#
#####################################################################

rule plot_international_workforce_distribution:
    input:
        PUB_AUTHOR_INTL,
        ST_GROUP,
        COLOR_SCHEME
    output:
        INTERNATIONAL_WORKFORCE_DISTRIBUTION_RAW,
        INTERNATIONAL_WORKFORCE_DISTRIBUTION_PROP
    shell:
        "python scripts/plot_workforce_distribution.py {input} {output}"
        
rule plot_authorship_distribution:
    input:
        PUB_AUTHOR_INTL_NOALPHA,
        ST_GROUP,
        COLOR_SCHEME
    output:
        AUTHORSHIP_DISTRIBUTION
    shell:
        "python scripts/plot_authorship_distribution.py {input} {output}"
        
rule reshuffle_authorship:
    input:
        PUB_AUTHOR_INTL_NOALPHA,
    output:
        PUB_AUTHOR_EXPECTED
    shell:
        "python scripts/reshuffle_author.py {input} {output}"
        
rule plot_representation_alltime:
    input:
        PUB_AUTHOR_INTL_NOALPHA,
        PUB_AUTHOR_EXPECTED,
        WORLD_SHP
    output:
        AUTHORSHIP_REPRESENTATION,
        AUTHORSHIP_REPRESENTATION_LEGEND
    shell:
        "python scripts/plot_representation_alltime.py {input} {output}"
        
rule plot_representation_overtime:
    input:
        PUB_AUTHOR_INTL_NOALPHA,
        PUB_AUTHOR_EXPECTED,
        ST_GROUP,
        COLOR_SCHEME
    output:
        AUTHORSHIP_REPRESENTATION_OVERTIME
    shell:
        "python scripts/plot_representation_overtime.py {input} {output}"
        
rule cal_first_last_pair:
    input:
        PUB_AUTHOR_INTL_NOALPHA
    output:
        FIRST_LAST_PAIR
    shell:
        "python scripts/cal_first_last_pair.py {input} {output}"
        
rule cal_pub_pair_raw:
    input:
        PUB_AUTHOR_INTL_NOALPHA
    output:
        PUB_PAIR_RAW
    shell:
        "python scripts/cal_pair_raw.py {input} {output}"
        
rule cal_conditional_pair:
    input:
        PUB_AUTHOR_INTL_NOALPHA
    output:
        FIXED_FIRST,
        FIXED_LAST,
    shell:
        "python scripts/cal_conditional_pair.py {input} {output}"

rule plot_fixed_first:
    input:
        PUB_PAIR_RAW,
        FIXED_FIRST,
        ST_GROUP,
        COLOR_SCHEME
    output:
        FIXED_FIRST_PLOT
    params:
        title='Country of the first author'
    shell:
        "python scripts/plot_normed_authorship_pair.py {input} {output} {params.title}"
        
    