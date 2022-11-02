project('test',
  'c',
  #default_options : ['c_std=c99']
  default_options : ['c_std=gnu17']
)

c_args = [
   '-O0', '-g',
   #'-std=c99',
   '-W', '-Wall', '-Wpointer-arith', '-Wno-unused-parameter', '-Wno-unused-but-set-variable', '-Wunused-function', '-Wno-unused-variable', '-Wno-unused-value',
   #'-Werror',
   '-fms-extensions',
]

# https://stackoverflow.com/questions/985403/seeing-expanded-c-macros
# https://stackoverflow.com/questions/70022733/dependency-and-option-in-meson-project
# meson build -Dmore=macro --wipe
if get_option('more') == 'macro'
  extra_args = ['-save-temps']
else
  extra_args = []
endif

add_project_arguments(c_args + extra_args, language: 'c')

#executable('t1exe', 't1.c', c_args : extra_args)
exe4 = executable('t4exe', 't4.c')
test('test4', exe4, args : ['--somearg'], env : ['ENVVAR=val'])

