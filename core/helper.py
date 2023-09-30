def debug_query(show_where=False):
    """
    log the query that use in a function
    you can use it as a decorator before your view like:
    @debug_query()
    def list(request, **):
    @param show_where: just show condition of queries
    @return:
    """

    def dec(func):
        def wrapper(
            *args,
            **kwargs,
        ):
            from django.db import reset_queries, connection
            import logging

            logging.basicConfig(
                format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
                level=logging.INFO,
                handlers=[logging.StreamHandler()],
            )
            logger = logging.Logger("test_query")
            reset_queries()
            res = func(*args, **kwargs)
            for query in connection.queries:
                sql, time = query.values()
                if show_where:
                    sql = sql[sql.find("WHERE") :]
                if len(sql) > 100:
                    __sql_str = """"""
                    for i in range((len(sql) // 150) + 1):
                        __sql_str += sql[i * 150 : (i + 1) * 150] + "\n"
                    sql = __sql_str
                if float(time) > 0.01:
                    logger.error(time)
                    logger.error(sql)

                else:
                    logger.warning(time)
                    logger.warning(sql)
            return res

        return wrapper

    return dec


def round_off_rating(number):
    """Round a number to the closest half integer.
    >>> round_off_rating(1.3)
    1.5
    >>> round_off_rating(2.6)
    2.5
    >>> round_off_rating(3.0)
    3.0
    >>> round_off_rating(4.1)
    4.0"""
    if number is None:
        return "None"
    return round(number * 2) / 2
