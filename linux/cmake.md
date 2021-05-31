http://derekmolloy.ie/hello-world-introductions-to-cmake/
[The sample code](https://github.com/derekmolloy/exploringBB/tree/master/extras/cmake)

# Usage

```shell

    $ tree studentlib_shared/
     studentlib_shared/
     |-- CMakeLists.txt
     |-- build
     |-- include
     |   \-- Student.h
     \-- src
     .   \-- Student.cpp
     3 directories, 3 files

    $ mkdir build; cd build
    $ cmake ..
    $ make
    $ sudo make install
    ...
    $ rm -fr build
```

## Demo lib + sample:

[add_subdirectory](https://cmake.org/examples/)

```shell

    toplevel-dir
    ..CMakeLists.txt
    ..Hello (lib)
    ....CMakeLists.txt
    ....hello.c
    ..Demo (exe)
    ....CMakeLists.txt
    ....demo.c
    ....demo_b.c

```

| tree of `Hello`    | CMakeLists.txt                                                                 |
| -----------        | -------------------                                                            |
| .                  |                                                                                |
| toplevel-dir       |                                                                                |
| ..CMakeLists.txt   | # CMakeLists files in this project can                                         |
| .                  | # refer to the root source directory of the project as ${HELLO_SOURCE_DIR} and |
| .                  | # to the root binary directory of the project as ${HELLO_BINARY_DIR}.          |
| .                  | cmake_minimum_required (VERSION 2.8.11)                                        |
| .                  | project (HELLO)                                                                |
| .                  |                                                                                |
| .                  | # Recurse into the "Hello" and "Demo" subdirectories. This does not actually   |
| .                  | # cause another cmake executable to run. The same process will walk through    |
| .                  | # the project's entire directory structure.                                    |
| .                  | add_subdirectory (Hello)                                                       |
| .                  | add_subdirectory (Demo)                                                        |
| .                  |                                                                                |
| ..Hello (lib)      |                                                                                |
| ....CMakeLists.txt |                                                                                |
| .                  | # Create a library called "Hello" which includes the source file "hello.cxx".  |
| .                  | # The extension is already found. Any number of sources could be listed here.  |
| .                  | add_library (Hello hello.c)                                                    |
| .                  |                                                                                |
| .                  | # Make sure the compiler can find include files for our Hello library          |
| .                  | # when other libraries or executables link to Hello                            |
| .                  | target_include_directories (Hello PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})          |
| .                  |                                                                                |
| ....hello.c        |                                                                                |
| ..Demo (exe)       |                                                                                |
| ....CMakeLists.txt | # Add executable called "helloDemo" that is built from the source files        |
| .                  | # "demo.cxx" and "demo_b.cxx". The extensions are automatically found.         |
| .                  | add_executable (helloDemo demo.c demo_b.c)                                     |
| .                  |                                                                                |
| .                  | # Link the executable to the Hello library. Since the Hello library has        |
| .                  | # public include directories we will use those link directories when building  |
| .                  | # helloDemo                                                                    |
| .                  | target_link_libraries (helloDemo LINK_PUBLIC Hello)                            |
| .                  |                                                                                |
| .                  |                                                                                |
| .                  |                                                                                |
| ....demo.c         |                                                                                |
| ....demo_b.c       |                                                                                |
|                    |                                                                                |
|                    |                                                                                |


## [share library with multiple executables]
(https://stackoverflow.com/questions/33443164/cmake-share-library-with-multiple-executables)


toplevel-dir
..CMakeLists.txt
..common (lib)
....CMakeLists.txt
....src
....include
..app1 (exe)
....CMakeLists.txt
....src
....include


| tree of `Project`  | CMakeLists.txt                                                                 |
| -----------        | -------------------                                                            |
| .                  |                                                                                |
| toplevel-dir       |                                                                                |
| ..CMakeLists.txt   |                                                                                |
| .                  | cmake_minimum_required (VERSION 3.1)                                           |
| .                  | project (toplevel)                                                             |
| .                  |                                                                                |
| .                  | add_subdirectory (common)                                                      |
| .                  | add_subdirectory (app1)                                                        |
| .                  |                                                                                |
| ..common (lib)     |                                                                                |
| ....CMakeLists.txt | cmake_minimum_required (VERSION 3.1)                                           |
| .                  | add_library (common STATIC common.c)                                           |
| .                  | target_include_directories (common PUBLIC "${CMAKE_CURRENT_LIST_DIR}/include") |
| .                  |                                                                                |
| ....src            |                                                                                |
| ....include        |                                                                                |
| .                  |                                                                                |
| ..app1 (exe)       |                                                                                |
| ....CMakeLists.txt | cmake_minimum_required (VERSION 3.1)                                           |
| .                  | project(app1)                                                                  |
| .                  |                                                                                |
| .                  | add_executable (${PROJECT_NAME} demo.c)                                        |
| .                  | target_link_libraries (${PROJECT_NAME} LINK_PUBLIC common)                     |
| .                  |                                                                                |
| ....src            |                                                                                |
| ....include        |                                                                                |
|                    |                                                                                |


## app base on two libs

https://stackoverflow.com/questions/11216408/cmake-dependencies-headers-between-apps-libraries-in-same-project


### project structure:

CMakeLists.txt
    lib1/CMakeLists.txt and all cpp and header files of the lib
    lib2/CMakeLists.txt and all cpp and header files of the lib
    app/CMakeLists.txt and all cpp and header files of the app


1. Toplevel: CMakeLists.txt:

```cmake
    cmake_minimum_required(VERSION 2.8 FATAL_ERROR)
    project(${PROJECT_NAME})
    add_subdirectory(lib1)
    add_subdirectory(lib2)
    add_subdirectory(app)
```

2. lib1/CMakeLists.txt:

```cmake
project(Lib1)
add_library(lib1 lib1.cpp lib1.h)
```

3. lib2/CMakeLists.txt:

    project(Lib2)
    add_library(lib2 lib2.cpp lib2.h)

    # Add /lib1 to #include search path
    include_directories(${Lib1_SOURCE_DIR})
    # Specify lib2's dependency on lib1
    target_link_libraries(lib2 lib1)

4. app/CMakeLists.txt:


    project(App)
    add_executable(app main.cpp some_header.h)

    # Add /lib1 and /lib2 to #include search path
    include_directories(${Lib1_SOURCE_DIR} ${Lib2_SOURCE_DIR})
    # Specify app's dependency on lib2.
    # lib2's dependency on lib1 is automatically added.
    target_link_libraries(app lib2)


5. For a relatively small project

There are plenty of different ways to achieve the same end result here.
For a relatively small project, I'd probably just use a single CMakeLists.txt:

```cmake
    cmake_minimum_required(VERSION 2.8 FATAL_ERROR)
    project(Test)

    add_library(lib1 lib1/lib1.cpp lib1/lib1.h)
    add_library(lib2 lib2/lib2.cpp lib2/lib2.h)
    add_executable(app app/main.cpp app/some_header.h)

    include_directories(${CMAKE_SOURCE_DIR}/lib1 ${CMAKE_SOURCE_DIR}/lib2)

    target_link_libraries(lib2 lib1)
    target_link_libraries(app lib2)
```

For further info on the relevant commands and their rationale, run:

cmake --help-command add_subdirectory
cmake --help-command include_directories
cmake --help-command target_link_libraries

## another sample

```shell
my_project
		├── build
		├── CMakeLists.txt
		├── hello_test
		│   ├── CMakeLists.txt
		│   └── main.cpp
		└── my_libs
			└── hello_lib
				├── CMakeLists.txt
				├── include
				│   └── hello.hpp
				└── src
					└── hello.cpp
```

The top level `CMakeList.txt` is as:

    cmake_minimum_required(VERSION 3.17.2)
    project(my_project)

    add_subdirectory(my_libs/hello_lib)
    add_subdirectory(hello_test)

The `hello_test/CMakeList.txt`:

    add_executable(hello_test main.cpp)
    target_link_libraries(hello_test PUBLIC hello_lib)

The `my_libs/hello_lib/CMakeList.txt`:

    add_library(
        hello_lib SHARED
        include/hello.hpp
        src/hello.cpp
    )

    target_include_directories(hello_lib PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/include")

## sample: not work
https://cmake.org/pipermail/cmake/2014-December/059248.html

The file structure:

    .
    |-- bin/
    |-- include/
    |   `-- mylib/
    |-- lib/
    `-- src/
        |-- CMakeLists.txt
        |-- mylib/
        |   |-- CMakeLists.txt
        |   |-- myfunc.cpp
        |   `-- myfunc.h
        `-- prog/
            |-- CMakeLists.txt
            `-- prog.cpp

The top level `src/CMakeList.txt` is as:

    cmake_minimum_required(VERSION 2.8.4)
    project(src)
    add_subdirectory(mylib)
    add_subdirectory(prog)

The `src/mylib/CMakeList.txt`:

    cmake_minimum_required(VERSION 2.8.4)
    project(mylib)

    set(CPP_SOURCE myfunc.cpp)
    set(HEADERS myfunc.h)

    add_library(mylib  ${CPP_SOURCE} )

    target_include_directories(
        mylib PUBLIC
        # Headers used from source/build location:
        "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>"
        # Headers used from the installed location:
        "$<INSTALL_INTERFACE:include>"
    )

    install(TARGETS mylib DESTINATION lib)
    install(FILES ${HEADERS} DESTINATION include/mylib)

The `src/prog/CMakeList.txt`:

    cmake_minimum_required(VERSION 2.8.4)
    project(prog)

    set(SOURCE_FILES prog.cpp)

    set(LIBS mylib)

    add_executable(prog ${SOURCE_FILES})
    target_link_libraries(prog  ${LIBS})
    install(TARGETS prog DESTINATION bin)

# Howtos

## howto print cmake vars


```cmake
macro(print_all_variables)
    message(STATUS "print_all_variables------------------------------------------{")
    get_cmake_property(_variableNames VARIABLES)
    foreach (_variableName ${_variableNames})
        message(STATUS "${_variableName}=${${_variableName}}")
    endforeach()
    message(STATUS "print_all_variables------------------------------------------}")
endmacro()


function(dump_cmake_variables)
    get_cmake_property(_variableNames VARIABLES)
    list (SORT _variableNames)
    foreach (_variableName ${_variableNames})
        if (ARGV0)
            unset(MATCHED)
            string(REGEX MATCH ${ARGV0} MATCHED ${_variableName})
            if (NOT MATCHED)
                continue()
            endif()
        endif()
        message(STATUS "${_variableName}=${${_variableName}}")
    endforeach()
endfunction()


### call like this:

print_all_variables()
dump_cmake_variables("^shmlib")

```

