from django.shortcuts import render
from django.views.generic import TemplateView
from .models import SocTable, LogTable, Reviews, SocMaster
from django.db.models import Count
from math import pi
import pandas as pd
from bokeh.io import output_file, save
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(TemplateView):
    template_name = 'home/home.html'


class SocView(LoginRequiredMixin, View):
    login_url = '/'
    template_name = 'home/society.html'

    def get(self, request, *args, **kwargs):

        output_file("templates/home/pie.html")

        data_list = SocTable.objects.raw("select id, division_name, count(*) as cnt from soc_table group by division_name")
        record_division_list = list()
        record_division_cnt = list()
        for data in data_list:
            record_division_list.append(data.division_name)
            record_division_cnt.append(data.cnt)

        data = {'Division_Name': record_division_list, 'Reg_Count': record_division_cnt}
        df = pd.DataFrame.from_dict(data)
        testdata = df.to_dict('list')
        a = testdata['Division_Name']
        b = testdata['Reg_Count']
        x = {x: y for x, y in zip(a, b)}
        print(x)

        data = pd.Series(x).reset_index(name='value').rename(columns={'index': 'country'})
        data['angle'] = data['value'] / data['value'].sum() * 2 * pi
        data['color'] = Category20c[len(x)]

        p = figure(plot_height=350, title="Division Chart", toolbar_location=None,
                   tools="hover", tooltips="@country: @value", x_range=(-0.5, 1.0))

        p.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend='country', source=data)

        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None
        save(p)

        # show(p)
        # print(p)
        return render(request, 'home/society.html', {"flag": False})

# code for second pie graph

    def post(self, request, *args, **kwargs):

        try:
            output_file("templates/home/pie1.html")

            request_data = request.POST
            divisionname = request_data['division_name']
            data_list = SocTable.objects.filter(division_name=divisionname).values('dist_name').annotate(Count('reg_no'))
            dist_name_list = list()
            reg_count_list = list()

            for data in data_list:
                dist_name_list.append(data['dist_name'])
                reg_count_list.append(data['reg_no__count'])

            data = {'District': dist_name_list, 'Registration_Count': reg_count_list}
            df1 = pd.DataFrame.from_dict(data)
            testdata = df1.to_dict('list')
            a = testdata['District']
            b = testdata['Registration_Count']
            soccount = sum(b)
            x = {x: y for x, y in zip(a, b)}
            print(x)

            data = pd.Series(x).reset_index(name='value').rename(columns={'index': 'country'})
            data['angle'] = data['value'] / data['value'].sum() * 2 * pi
            data['color'] = Category20c[len(x)]

            p = figure(plot_height=350, title="District Chart", toolbar_location=None,
                       tools="hover", tooltips="@country: @value", x_range=(-0.5, 1.0))

            p.wedge(x=0, y=1, radius=0.4,
                    start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                    line_color="white", fill_color='color', legend='country', source=data)

            p.axis.axis_label = None
            p.axis.visible = False
            p.grid.grid_line_color = None
            #show(p)
            save(p)
            return render(request, 'home/society.html', {"flag": True})

        except:

            return render(request, 'home/society.html', {"flag": False})

#
# def society(request):
#     return render(request, 'home/society.html', {})


class UserView(LoginRequiredMixin, View):
    login_url = '/'
    template_name = 'home/Test/user.html'

    def get(self, request, *args, **kwargs):
        from bokeh.io import save, output_file
        from bokeh.models import ColumnDataSource
        from bokeh.palettes import Spectral10
        from bokeh.plotting import figure
        from bokeh.transform import factor_cmap

        output_file("templates/home/bar1.html")

        data_list = LogTable.objects.all().values('user_name', 'trk_ip_address').annotate(
                Count('user_name')).order_by('-user_name__count')[1:11]
        record_user_name = list()
        record_count_user_name = list()

        for data in data_list:
            record_user_name.append(data['user_name'])
            record_count_user_name.append(data['user_name__count'])

        data = {'User_name': record_user_name, 'Count_Number': record_count_user_name}
        df1 = pd.DataFrame.from_dict(data)
        testdata = df1.to_dict('list')
        username = testdata['User_name']
        print(username)
        counts = testdata['Count_Number']
        print(counts)
        source = ColumnDataSource(data=dict(username=username, counts=counts))

        p = figure(x_range=username, plot_height=500, toolbar_location=None, title="RFSC User Visits Count")
        p.vbar(x='username', top='counts', width=0.9, source=source, legend="username",
               line_color='white', fill_color=factor_cmap('username', palette=Spectral10, factors=username))

        p.xgrid.grid_line_color = None
        p.y_range.start = 10
        p.y_range.end = 100
        p.legend.orientation = "horizontal"
        p.legend.location = "top_center"
        p.xaxis.major_label_orientation = "vertical"
        p.height = 300
        p.width = 600
        save(p)

        #for second user analysis graph

        output_file("templates/home/bar2.html")

        data_list1 = LogTable.objects.all().values('trk_ip_address').annotate(
                     Count('trk_ip_address')).order_by('-trk_ip_address__count')[1:11]
        record_ip_name = list()
        record_count_ip_name = list()

        for data in data_list1:
            record_ip_name.append(data['trk_ip_address'])
            record_count_ip_name.append(data['trk_ip_address__count'])

        data1 = {'trk_ip_address': record_ip_name, 'Count_Number': record_count_ip_name}
        df2 = pd.DataFrame.from_dict(data1)
        df2 = df2[['trk_ip_address', 'Count_Number']]
        testdata1 = df2.to_dict('list')
        ipname = testdata1['trk_ip_address']
        print(ipname)
        counts = testdata1['Count_Number']
        print(counts)
        source = ColumnDataSource(data=dict(ipname=ipname, counts=counts))

        p1 = figure(x_range=ipname, plot_height=500, toolbar_location=None, title="RFSC IP Visits Count")
        p1.vbar(x='ipname', top='counts', width=0.9, source=source, legend="ipname",
                line_color='white', fill_color=factor_cmap('ipname', palette=Spectral10, factors=ipname))

        p1.xgrid.grid_line_color = None
        p1.y_range.start = 50
        p1.y_range.end = 500
        p1.legend.orientation = "horizontal"
        p1.legend.location = "top_center"
        p1.xaxis.major_label_orientation = "vertical"
        p1.height = 300
        p1.width = 600
        save(p1)

        # for third user analysis graph
        output_file("templates/home/bar3.html")

        data_list3 = LogTable.objects.raw(
                 "SELECT User_id, User_name, TIMEDIFF(LogOut_time,Time_login) as time_diff FROM log_table"
                 " WHERE TIMEDIFF(LogOut_time,Time_login) IS NOT NULL"
                 " ORDER BY TIMEDIFF(LogOut_time,Time_login) DESC LIMIT 10")
        print(data_list3)
        record_user_name = list()
        recorde_trk_time = list()

        for data3 in data_list3:
            record_user_name.append(data3.user_name)
            recorde_trk_time.append(int(str(data3.time_diff).split(':')[0]))
        data3 = {'user_name': record_user_name, 'session_time': recorde_trk_time}
        df3 = pd.DataFrame.from_dict(data3)
        df3 = df3[['user_name', 'session_time']]
        testdata3 = df3.to_dict('list')
        username = testdata3['user_name']
        print(username)
        counts = testdata3['session_time']
        print(counts)
        source = ColumnDataSource(data=dict(username=username, counts=counts))

        p3 = figure(x_range=username, plot_height=500, toolbar_location=None, title="RFSC User Session Count")
        p3.vbar(x='username', top='counts', width=0.9, source=source, legend="username",
                line_color='white', fill_color=factor_cmap('username', palette=Spectral10, factors=username))

        p3.xgrid.grid_line_color = None
        p3.y_range.start = 1
        p3.y_range.end = 24
        p3.legend.orientation = "horizontal"
        p3.legend.location = "top_center"
        p3.xaxis.major_label_orientation = "vertical"
        p3.height = 300
        p3.width = 600
        save(p3)

        return render(request, 'home/user.html', {})


class ReportView(LoginRequiredMixin, View):
    login_url = '/'
    template_name = 'home/report.html'

    def get(self, request, *args, **kwargs):
        from bokeh.plotting import figure, save, output_file
        from bokeh.tile_providers import CARTODBPOSITRON

        output_file("templates/home/tile.html")

        # range bounds supplied in web mercator coordinates
        p = figure(x_range=(8400000, 9600000), y_range=(2800000, 3400000),
                   x_axis_type="mercator", y_axis_type="mercator")
        p.add_tile(CARTODBPOSITRON)
        p.height = 450
        p.width = 650

        save(p)

        return render(request, 'home/report.html')


class MonthView(LoginRequiredMixin, View):
    login_url = '/'
    template_name = 'home/month.html'

    def get(self, request, *args, **kwargs):

        from bokeh.palettes import Spectral11
        from bokeh.plotting import figure, save, output_file
        from bokeh.models import ColumnDataSource

        output_file("templates/home/temp.html")

        data_list = SocTable.objects.raw('SELECT id, COUNT(*) as cnt, MONTHNAME(reg_date) as rd_month '
                                         'FROM soc_table GROUP BY MONTH(reg_date)')
        record_month_list = list()
        record_month_cnt = list()

        for data in data_list:
            record_month_list.append(data.rd_month)
            record_month_cnt.append(data.cnt)

        data = {'Month_Name': record_month_list, 'Reg_Count': record_month_cnt}
        df = pd.DataFrame.from_dict(data)
        print(df)
        df = df[['Month_Name', 'Reg_Count']]
        testdata = df.to_dict('list')
        monthvalue = testdata['Month_Name']
        print(monthvalue)
        counts = testdata['Reg_Count']
        print(counts)

        p = figure(plot_width=300, plot_height=100)
        x = monthvalue
        y = counts
        p = figure(x_range=x)
        p.line(x, y)
        p.circle(x, y, fill_color="white", size=8)
        p.height = 400
        p.width = 600
        save(p)

        return render(request, 'home/month.html')


class PredictView(LoginRequiredMixin, View):
    login_url = '/'
    template_name = 'home/predict.html'

    def get(self, request, *args, **kwargs):
        import matplotlib.pyplot as plt
        import numpy as np
        from bokeh.palettes import Spectral11
        from bokeh.plotting import figure, save, output_file

        output_file("templates/home/temp2.html")
        x = [962, 556, 366, 792, 652, 320, 622, 425]

        toy_df = pd.DataFrame(data=np.array(x), columns=['a'],
                              index=pd.DatetimeIndex(start='01-01-2011', periods=len(x), freq='y'))

        numlines = len(toy_df.columns)
        mypalette = Spectral11[0:numlines]

        p = figure(width=500, height=300, x_axis_type="datetime")
        p.multi_line(xs=[toy_df.index.values] * numlines,
                     ys=[toy_df[name].values for name in toy_df],
                     line_color=mypalette,
                     line_width=5)
        save(p)

        def linreg(X, Y):
            """
            return a,b in solution to y = ax + b such that root mean square distance between trend line and original points is minimized
            """
            N = len(X)
            Sx = Sy = Sxx = Syy = Sxy = 0.0
            for x, y in zip(X, Y):
                Sx = Sx + x
                Sy = Sy + y
                Sxx = Sxx + x * x
                Syy = Syy + y * y
                Sxy = Sxy + x * y
            det = Sxx * N - Sx * Sx
            return (Sxy * N - Sy * Sx) / det, (Sxx * Sy - Sx * Sxy) / det

        x1 = [962, 556, 366, 792, 652, 320, 622, 425]
        x2 = []
        for i in range(5):
            a, b = linreg(range(len(x1)), x1)
            # value of predicted year as 'b'
            #	print(a ," ", b)
            x1.append(b)
            x2.append(b)
            print(x2)

        output_file("templates/home/temp1.html")

        toy_df = pd.DataFrame(data=np.array(x1), columns=['a'],
                              index=pd.DatetimeIndex(start='01-01-2011', periods=len(x1), freq='y'))

        numlines = len(toy_df.columns)
        mypalette = Spectral11[0:numlines]

        p = figure(width=500, height=300, x_axis_type="datetime")
        p.multi_line(xs=[toy_df.index.values] * numlines,
                     ys=[toy_df[name].values for name in toy_df],
                     line_color='red',
                     line_width=5)
        save(p)

        return render(request, 'home/predict.html')


class ReviewView (LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request, *args, **kwargs):
        return render(request, 'home/review.html', {"flag": False})

    def post(self, request, *args, **kwargs):
        username = request.POST['user_name']
        age = request.POST['age']
        comments = request.POST['comments']
        ratings = request.POST['rating']
        s = Reviews(user_name=username, age=age, comments=comments, rate=ratings)
        s.save()
        return render(request, 'home/review.html', {"flag": True})


class RegDurPageView(LoginRequiredMixin, View):
    login_url = '/'
    template_name = 'home/regduration.html'

    def get(self, request, *args, **kwargs):
        from bokeh.io import save, output_file
        from bokeh.plotting import figure
        output_file("templates/home/bar5.html")

        data_list = SocMaster.objects.raw("select id, division_name, round(abs(avg(datediff(app_date,reg_date)))) as 'duration' from soc_master group by division_name")
        record_division_list = list()
        record_duration_cnt = list()
        for data in data_list:
            record_division_list.append(data.division_name)
            record_duration_cnt.append(data.duration)
        data = {'Division_Name': record_division_list, 'Duration_Count': record_duration_cnt}
        df = pd.DataFrame.from_dict(data)
        print(df)
        testdata = df.to_dict('list')
        divisionname = testdata['Division_Name']
        duration = testdata['Duration_Count']

        p = figure(x_range=divisionname, plot_height=400, title="Average Duration in Days",
                   toolbar_location=None, tools="")

        p.vbar(x=divisionname, top=duration, width=0.9)

        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        p.xaxis.major_label_orientation = "vertical"

        save(p)

        return render(request, 'home/regduration.html', {"flag": False})

    def post(self, request, *args, **kwargs):

        from bokeh.io import save, output_file
        from bokeh.plotting import figure

        output_file("templates/home/bar6.html")
        request_data = request.POST
        divisionname = request_data['division_name']
        data_list = SocMaster.objects.raw("select id, dist_name, round(abs(avg(datediff(app_date,reg_date)))) as 'duration' from soc_master where division_name = '"+(divisionname)+"' group by dist_name")
        record_district_list = list()
        record_duration_cnt = list()
        for data in data_list:
            record_district_list.append(data.dist_name)
            record_duration_cnt.append(data.duration)

        data = {'District_Name': record_district_list, 'Duration_Count': record_duration_cnt}
        df1 = pd.DataFrame.from_dict(data)
        print(df1)
        testdata = df1.to_dict('list')
        districtname = testdata['District_Name']
        duration = testdata['Duration_Count']

        p = figure(x_range=districtname, plot_height=400, title="Average Duration in Days",
                   toolbar_location=None, tools="")

        p.vbar(x=districtname, top=duration, width=0.9)

        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        p.xaxis.major_label_orientation = "vertical"

        save(p)

        return render(request, 'home/regduration.html', {"flag": True})


class SocTypeView(LoginRequiredMixin, View):
    login_url = '/'
    template_name = 'home/societytype.html'

    def get(self, request, *args, **kwargs):
        output_file("templates/home/pie2.html")

        data_list = SocMaster.objects.raw("select id, stype_name, count(*) as cnt from soc_master group by stype_name")
        record_stype_list = list()
        record_reg_cnt = list()
        for data in data_list:
            record_stype_list.append(data.stype_name)
            record_reg_cnt.append(data.cnt)

        data = {'Stype_Name': record_stype_list, 'Reg_Count': record_reg_cnt}
        df = pd.DataFrame.from_dict(data)
        testdata = df.to_dict('list')
        a = testdata['Stype_Name']
        b = testdata['Reg_Count']
        x = {x: y for x, y in zip(a, b)}
        print(x)

        data = pd.Series(x).reset_index(name='value').rename(columns={'index': 'country'})
        data['angle'] = data['value'] / data['value'].sum() * 2 * pi
        data['color'] = Category20c[len(x)]

        p = figure(plot_height=350, title="Society Type Chart", toolbar_location=None,
                   tools="hover", tooltips="@country: @value", x_range=(-0.5, 1.0))

        p.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend='country', source=data)

        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None
        save(p)

        return render(request, 'home/societytype.html', {"flag": False})

    def post(self, request, *args, **kwargs):

        output_file("templates/home/barsoctype.html")
        request_data = request.POST
        districtname = request.POST['dist_name']
        divisionname = request_data['division_name']
        data_list = SocTable.objects.filter(division_name=divisionname, dist_name=districtname).values('stype_name').annotate(Count('stype_name'))
        stype_name_list = list()
        stype_count_list = list()

        for data1 in data_list:
            stype_name_list.append(data1['stype_name'])
            stype_count_list.append(data1['stype_name__count'])

        data1 = {'Society_Type': stype_name_list, 'Registration_Count': stype_count_list}
        df1 = pd.DataFrame.from_dict(data1)
        testdata = df1.to_dict('list')
        a = testdata['Society_Type']
        b = testdata['Registration_Count']

        p = figure(x_range=a, plot_height=400, title="Types of society",
                   toolbar_location=None, tools="")

        p.vbar(x=a, top=b, width=0.9)

        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        p.xaxis.major_label_orientation = "horizontal"

        save(p)

        return render(request, 'home/societytype.html', {"flag": True})


class SuccessView(LoginRequiredMixin, TemplateView):
    login_url = '/'
    template_name = 'portal/success.html'


# class CurrMonthView(LoginRequiredMixin, TemplateView):
#     login_url = '/'
#     template_name = 'home/currmonth.html'
#
#     def get(self, request, *args, **kwargs):
#
#         from bokeh.palettes import Spectral11
#         from bokeh.plotting import figure, save, output_file
#         from bokeh.models import ColumnDataSource
#
#         output_file("templates/home/temp.html")
#
#         data_list = SocTable.objects.raw('SELECT id, COUNT(*) as cnt, MONTHNAME(reg_date) as rd_month '
#                                          'FROM soc_table GROUP BY MONTH(reg_date)')
#         record_month_list = list()
#         record_month_cnt = list()
#
#         for data in data_list:
#             record_month_list.append(data.rd_month)
#             record_month_cnt.append(data.cnt)
#
#         data = {'Month_Name': record_month_list, 'Reg_Count': record_month_cnt}
#         df = pd.DataFrame.from_dict(data)
#         print(df)
#         df = df[['Month_Name', 'Reg_Count']]
#         testdata = df.to_dict('list')
#         monthvalue = testdata['Month_Name']
#         print(monthvalue)
#         counts = testdata['Reg_Count']
#         print(counts)
#
#         p = figure(plot_width=300, plot_height=100)
#         x = monthvalue
#         y = counts
#         p = figure(x_range=x)
#         p.line(x, y)
#         p.circle(x, y, fill_color="white", size=8)
#         p.height = 400
#         p.width = 600
#         save(p)
#         return render(request, 'home/month.html')
