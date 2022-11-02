src_libhello = ['Hello.cpp', 'add.h', 'answer.c', 'answer.h']

libhello = static_library('runtime',
                            src_libhello,
                            install : true)

executable('statically-linked', 'main.c',
           link_with: tq84_lib_static)

executable('use-shared-library', 'main.c',
           link_with: tq84_lib_shared)


cc = meson.get_compiler('c')
libdl = cc.find_library('dl')
executable('dynamic-library-loader', 'dynamic-library-loader.c',
           dependencies: libdl)
