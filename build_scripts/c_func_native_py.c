struct pypy_rpy_string0* pypy_g_python_executer(
    struct pypy_rr_compiler_datatypes_W_Root0 *l_some_code_1,
    struct pypy_rr_compiler_datatypes_W_Root0 *l_variables_4)
{
    struct pypy_rpy_string0 *out = NULL;

    if (!l_some_code_1)
        return NULL;

    struct pypy_rpy_string0 *rpy_str =
        ((struct pypy_rr_compiler_datatypes_W_String0*)l_some_code_1)->ws_inst_stringval;

    if (!rpy_str || !rpy_str->rs_chars.items)
        return NULL;

    const char *code_cstr = rpy_str->rs_chars.items;

    // Eliminăm ghilimelele exterioare dacă există
    size_t len = strlen(code_cstr);
    char *buf = NULL;
    if (len >= 2 && code_cstr[0] == '"' && code_cstr[len - 1] == '"') {
        buf = malloc(len - 1); // len-2 + \0
        if (!buf) return NULL;
        memcpy(buf, code_cstr + 1, len - 2);
        buf[len - 2] = '\0';
        code_cstr = buf;
    }

    // Print codul Python care urmează să fie executat
    printf("Execut codul Python:\n%s\n", code_cstr);

    if (!Py_IsInitialized()) Py_Initialize();

    PyObject *globals_dict = PyDict_New();
    PyObject *locals_dict = PyDict_New();
    if (!globals_dict || !locals_dict) {
        Py_XDECREF(globals_dict);
        Py_XDECREF(locals_dict);
        free(buf);
        return NULL;
    }

    // Importăm sys și io pentru a captura stdout
    PyObject *sys = PyImport_ImportModule("sys");
    PyObject *io = PyImport_ImportModule("io");
    PyObject *stringio = PyObject_CallMethod(io, "StringIO", NULL);
    if (!sys || !io || !stringio) goto cleanup;

    // Salvăm stdout original și îl înlocuim
    PyObject *stdout_orig = PyObject_GetAttrString(sys, "stdout");
    PyObject_SetAttrString(sys, "stdout", stringio);

    // Executăm codul Python
    PyObject *py_ret = PyRun_StringFlags(code_cstr, Py_file_input, globals_dict, locals_dict, NULL);

    // Obținem conținutul bufferului StringIO
    PyObject *value = PyObject_CallMethod(stringio, "getvalue", NULL);
    if (value && PyUnicode_Check(value)) {
        const char *s = PyUnicode_AsUTF8(value);
        size_t len_out = strlen(s);
        out = malloc(sizeof(struct pypy_rpy_string0) + len_out + 1);
        if (out) {
            out->rs_chars.length = len_out;
            memcpy(out->rs_chars.items, s, len_out + 1);
            out->rs_hash = 0;
        }
    }

    // Restaurăm stdout original
    PyObject_SetAttrString(sys, "stdout", stdout_orig);

    // Curățenie
    Py_XDECREF(py_ret);
    Py_XDECREF(stdout_orig);
    Py_XDECREF(value);
    Py_XDECREF(stringio);
    Py_XDECREF(io);
    Py_XDECREF(sys);

cleanup:
    Py_DECREF(globals_dict);
    Py_DECREF(locals_dict);

    // Print rezultatul
    if (out && out->rs_chars.items)
        printf("Rezultat:\n%s\n", out->rs_chars.items);

    free(buf); // eliberăm bufferul temporar dacă a fost alocat
    return out;
}
