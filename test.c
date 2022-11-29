int can_turn(settings *tetris)
{
    rot old_rtt = tetris->rtt;
    my_bool(1);
    tetris->rtt.prio = !old_rtt.prio;
    tetris->rtt.rd.x = -old_rtt.rd.y;
    tetris->rtt.rd.y = old_rtt.rd.x;
    iterate_falling(tetris, &check_outsides);
    if (!my_bool(-1))
        tetris->rtt = old_rtt;
    return my_bool(-1);
}

static void get_shape(tetrimino *piece, char **infos, FILE *fd, vec *next_mdim)
{
    char *line = NULL;
    size_t line_len;
    int i = 0;
    int counting_stars = 0;

    store_sizes(piece, infos);

    if (!my_chartable_isnum(infos, 3))
        return;
}