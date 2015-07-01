# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ibati.models import Category, Label, Post, JobTitle, Member, Slider, User, Link
from ibati.extensions import db

def init_post(session):

    about_us = Category(name='about-us', cname='单位简介', order=50)
    session.add(about_us)

    news = Category(name='news', cname='新闻通知', order=100)
    session.add(news)
    dispatch = Label(name='dispatch', cname='快讯新闻', order=100, category=news)
    session.add(dispatch)
    notice = Label(name='notice', cname='通知公告', order=200, category=news)
    session.add(notice)
    report = Label(name='report', cname='学术报告', order=300, category=news)
    session.add(report)

    research = Category(name='research', cname='科学研究', order=400)
    session.add(research)
    area = Label(name='area', cname='研究方向', order=200, category=research)
    session.add(area)
    project = Label(name='project', cname='科研项目', order=300, category=research)
    session.add(project)
    equipment = Label(name='equipment', cname='科研设备', order=400, category=research)
    session.add(equipment)

    member = Category(name='member', cname='研究队伍', order=500)
    session.add(member)
    teacher = Label(name='teacher', cname='教师', order=100, category=member)
    session.add(teacher)
    postdoctor = Label(name='postdoctor', cname='博士后', order=150, category=member)
    session.add(postdoctor)
    professor = Label(name='professor', cname='客座教授', order=200, category=member)
    session.add(professor)
    visiting_scholar = Label(name='visiting-scholar', cname='访问学者', order=300, category=member)
    session.add(visiting_scholar)

    achievement = Category(name='achievement', cname='研究成果', order=520)
    session.add(achievement)
    paper = Label(name='paper', cname='论文', order=100, category=achievement)
    session.add(paper)
    patent = Label(name='patent', cname='专利', order=200, category=achievement)
    session.add(patent)
    monograph = Label(name='monograph', cname='专著', order=250, category=achievement)
    session.add(monograph)
    other = Label(name='other', cname='其他', order=300, category=achievement)
    session.add(other)

    postgraduate = Category(name='postgraduate', cname='研究生培养', order=600)
    session.add(postgraduate)
    enrolling = Label(name='enrolling', cname='研究生招生', order=100, category=postgraduate)
    session.add(enrolling)
    candidate = Label(name='candidate', cname='在读研究生', order=200, category=postgraduate)
    session.add(candidate)
    graduated = Label(name='graduated', cname='毕业研究生', order=300, category=postgraduate)
    session.add(graduated)

    teaching = Category(name='teaching', cname='教学工作', order=700)
    session.add(teaching)
    undergraduate = Label(name='undergraduate', cname='本科生教学', order=100, category=teaching)
    session.add(undergraduate)
    postgraduate = Label(name='postgraduate', cname='研究生教学', order=200, category=teaching)
    session.add(postgraduate)

    inter_coop = Category(name='inter-coop', cname='国际合作', order=720)
    session.add(inter_coop)

    recruitment = Category(name='recruitment', cname='人员招聘', order=800)
    session.add(recruitment)

    for _ in range(20):
        p = Post(
            title='西安交大参加教育部深化高等学校创新创业教育改革视频会议',
            content=('2015年6月2日，教育部组织召开深化高等学校创新创业教育改革视频会议，'
                     '西安交大校长王树国、党委副书记宫辉、副校长郑庆华以及'
                     '教务处、研究生院、就业中心、科研院、人力资源部、财务处、学生处、团委、工程坊、科技园、各书院负责人'
                     '和创新创业教育教师代表40余人全程参会。'
                     '为深入贯彻落实《国务院办公厅关于深化高等学校创新创业教育改革的实施意见》(以下简称《实施意见》)，'
                     '教育部组织召开深化高等学校创新创业教育改革视频会议，对深化高校创新创业教育改革工作进行动员部署，'
                     '努力造就大众创业、万众创新的生力军，为国家实施创新驱动发展战略提供人才智力支撑。'
                     '教育部袁贵仁部长等教育部负责同志、教育部相关部门机构、各省教育行政部门和教育部直属高校等'
                     '共7600余人参加大会。'),
            category=news, label=dispatch
        )
        db.session.add(p)

    p = Post(
        title='单位简介',
        content=('西安交通大学 生物医学分析技术与仪器研究所'
                 'Institute of Biomedical Analytical Technology and Instrumentation'
                 '生物医学分析技术及仪器研究所是根据国家十一五发展规划和生命科学与技术学院整体发展需要，'
                 '通过学院整合于2007年6月15日成立。目标是充分发挥学科交叉的作用，'
                 '在生物医学分析技术与仪器的基础理论研究、应用研究、人才培养、促进相应技术转化为生产力等方面取得显著进展。'
                 '该所现有教职工12人，其中教授5人，副教授3 人和高级工程师1人，讲师3位。'
                 '目前承担和完成了国家自然科学基金近30项（包括重点项目、国际合作）、国家科技部863项目、国家重大科学仪器设备开发项目、'
                 '陕西省自然科学基金项目、西安市科技攻关项目、横向课题数十项等。'
                 '目前的研究方向有生物医学光子学影像与光谱分析技术、基于多信息融合的生物荧光探针和光学传感器、先进敏感分析技术及仪器等。'
                 '目前研究的重点项目包括有：基于多光谱荧光成像的在体三维光学标测系统、基于新型光穿孔技术的纳米尺度细胞膜微手术研究、'
                 '金纳米棒靶向的激光细胞微手术及其机理研究、纳米材料的界观和微观效应及机理、基于纳米金探针的肿瘤细胞示踪等研究。'
                 '研究所现有博士和硕士研究生80多名。'),
        category=about_us
    )
    db.session.add(p)
    db.session.commit()



def init_member(session):
    teacher = JobTitle(name='教师')
    session.add(teacher)

    student = JobTitle(name='学生')
    session.add(student)

    zhaolinger = Member(name='赵灵儿', job_title=student, intro='西安交通大学软件学院学生', photo='uploads/200800000006.jpg')
    session.add(zhaolinger)
    linyueru = Member(name='林月如', job_title=student, intro='西安交通大学软件学院学生', photo='uploads/200800000012.jpg')
    session.add(linyueru)
    anu = Member(name='阿奴', job_title=student, intro='西安交通大学软件学院学生', photo='uploads/200800000020.jpg')
    session.add(anu)
    wuhou = Member(name='巫后', job_title=teacher, intro='西安交通大学软件学院老师', photo='uploads/200800000123.jpg')
    session.add(wuhou)

    session.commit()


def init_home(session):
    slider_1 = Slider(
        title='心肌细胞实验',
        subtitle='心肌细胞电学特性和力学特性就耦合起来。但由于心血管疾病会改变力学或电学特性，因此这就很有研究的价值。',
        image='/static/images/content/052502.jpg', order=100, enable=True
    )
    session.add(slider_1)

    slider_2 = Slider(
        title='皮肤热疼痛实验',
        subtitle='由此建立了热-力-电（疼痛）多场耦合行为理论，为有效指导激光、微波等临床热疗技术及镇痛方案提供了理论依据。',
        image='/static/images/content/052210.jpg', order=200, enable=True
    )
    session.add(slider_2)

    slider_3 = Slider(
        title='标题3',
        subtitle='',
        image='/static/images/content/051903.jpg', order=300, enable=True
    )
    session.add(slider_3)

    session.commit()

    init_links(session)
    init_account(session)


def init_links(session):
    for i in range(5):
        l = Link(name='友情链接', href='http://www.xjtu.edu.cn', order=i)
        session.add(l)
    session.commit()


def init_account(session):
    username = None
    password = None
    password_confirm = None

    while not username:
        username = raw_input('Admin username: ')

    while not password or not password_confirm or password_confirm != password:
        password = raw_input('Admin password: ')
        password_confirm = raw_input('Confirm password: ')

    u = User(username=username, password=password)
    session.add(u)
    session.commit()

