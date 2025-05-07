struct wad_print_helper {
    void *data;
    void (*printer)(struct wad_print_helper *ph, const char *fmt, ...)
        __attribute__((__format__(__printf__, 2, 3)));
};

struct wad_glob_max {
    uint64_t max;
};
struct wad_stats_s_http_engine {
    struct {
        uint64_t total_req;
        uint64_t served_req;
        uint64_t total_server;
        uint64_t active_server;
    } http_1way_svr;

    struct {
        uint64_t total_req;
        WAD_STATS_INT(64, total_sessions)
        WAD_STATS_INT(64, http_0_9_req) WAD_STATS_STRUCT_END(http)
            WAD_STATS_STRUCT_START(webcache) WAD_STATS_INT(64, total_req)
                WAD_STATS_INT(32, concurrent_req) WAD_STATS_STRUCT_END(webcache)
                    WAD_STATS_STRUCT_START(web_proxy)
                        WAD_STATS_INT(64, total_req)
                            WAD_STATS_INT(64, total_sessions)
                                WAD_STATS_INT(32, concurrent_req)
                                    WAD_STATS_INT(32, concurrent_sessions)
                                        WAD_STATS_STRUCT_END(web_proxy)
                                            WAD_STATS_STRUCT_START(error)
                                                WAD_STATS_INT(64, http_0_9)
                                                    WAD_STATS_STRUCT_END(error)
                                                        WAD_STATS_STRUCT_SUB(
                                                            http2, http2)
    };

    void WAD_STATS_ADD_FUNC(http_engine)(
        int itr, bool recursive, void *dst, void *src);
    void WAD_STATS_PRINT_FUNC(http_engine)(
        const char *prefix, bool recursive, void *src,
        struct wad_print_helper *ph);
    int WAD_STATS_CLEAR_FUNC(http_engine)(bool recursive, void *src);
    WAD_STATS_DECLARE(diag)
