# AutoTestPlatform
基于图像识别的自动测试框架


FEATURES:
    基于图像是别的方式，即可以完全黑盒的做测试。

TODO:
    最终:将测试流程 状态机化。 
        状态机ui，运行时

    测试模块复用，基于图像的类使用.
        { src='skill1.png', type='img'}.click()
        { src='login.png', type='img',
            childs={
                ['password'] = 'input'
            }
        }.password.text = '123456'

    图像识别方式:
        template match, feature detection