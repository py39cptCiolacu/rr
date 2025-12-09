struct pypy_rpy_string0 *pypy_g_execute_python(struct pypy_rpy_string0 *l_v50788) {
    long len = RPyField(l_v50788, rs_chars).length;
    
    char buffer[8192];
    if (len >= 8192) {
        printf("Input too large!\n");
        return l_v50788;
    }

    for (long i = 0; i < len; i++) {
        buffer[i] = RPyField(l_v50788, rs_chars).items[i];
    }
    buffer[len] = '\0';

    char *clean = buffer;
    if (clean[0] == '"' && clean[len - 1] == '"') {
        clean[len - 1] = '\0';
        clean = clean + 1;
    }

    char escaped[9000];
    int pos = 0;
    for (int i = 0; clean[i] != '\0'; i++) {
        if (clean[i] == '"') {
            escaped[pos++] = '\\';
        }
        escaped[pos++] = clean[i];
    }
    escaped[pos] = '\0';

    printf("Executing Python code (cleaned):\n%s\n", escaped);

    char cmd[10000];
    snprintf(cmd, sizeof(cmd), "python3 -c \"%s\"", escaped);

    int ret = system(cmd);
    if (ret != 0) {
        printf("Python3 exited with code %d\n", ret);
    }

    return l_v50788;
}
