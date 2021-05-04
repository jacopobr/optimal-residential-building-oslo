__author__ = 'lorenzo'
import pandas as pd
from matplotlib import pyplot as plt
from math import *
import pvlib
import cmath


def ruiz(df):
    df['k_d']=0.944-1.538*exp(-exp(2.808-5.759*df['k_t']+2.276*pow(df['k_t'],2)-0.125*df['m']+0.013*pow(df['m'],2)))
    if df['ghi'] >= 8 and df['zenith'] <= 85 and df['k_t'] <= 1.2:
    #if df['ghi'] >= 8 and df['k_t'] <= 1.2:
        df['dhi'] = df['k_d']*df['ghi']
        df['dni'] = (df['ghi']-df['dhi'])/cos(radians(df['zenith']))
    return df


def Skartevit1(df):

    k1=0.87-0.56*exp(-0.06*df['altitude'])
    k0=0.2
    d1=0.15+0.43*exp(-0.06*df['altitude'])
    a=0.27
    a1=df['k_t']-k0
    b1=k1-k0
    k=0.5*(1+sin(radians(3.14*(a1/b1-0.5))))
    a11=1.09*k1-k0
    k11=0.5*(1+sin(radians(3.14*(a11/b1-0.5))))
    eps=1-(1-d1)*(a*pow(k11,0.5)+(1-a)*pow(k11,2))
    if df['k_t']<k0:
        fi=1
    if k0 <= df['k_t'] <= 1.09*k1:
        fi=1-(1-d1)*(a*pow(k,0.5)+(1-a)*pow(k,2))
    if df['k_t'] > 1.09*k1:
        fi=1-(1.09*k1*(1-eps))/df['k_t']
    if df['ghi'] >= 8 and df['zenith'] <= 85 and df['k_t'] <= 1.2:
        df['dni']=df['ghi']*(1-fi)/sin(radians(df['altitude']))
        df['dhi']=df['ghi']-df['dni']*cos(radians(df['zenith']))
    return df



    
def Skartevit11(df):
    if df['ghi'] >= 8 and df['zenith'] <= 85 and df['k_t'] <= 1.2:
        k1=0.87-0.56*exp(-0.06*df['altitude'])
        k0=0.2
        d1=0.15+0.43*exp(-0.06*df['altitude'])
        a=0.27
        alfa=1.09
        k=0.5*(1+sin(pi*((df['k_t']-k0)/(k1-k0)-0.5)))
        if df['k_t']<k0:
            df['k_d']=1
        if k0 <= df['k_t'] <= alfa*k1:
            df['k_d']=1-(1-d1)*(a*pow(k,0.5)+(1-a)*pow(k,2))
        if df['k_t'] > alfa*k1:
            K1 = 0.5*(1+sin(pi*((alfa*k1-k0)/(k1-k0)))-0.5)
            fk=1-(1-d1)*(a*sqrt(K1)+(1-a)*K1**2)
            df['k_d']=1-alfa*k1*(1-fk)/df['k_t']             
        df['dhi'] = df['k_d']*df['ghi']
        df['dni'] = (df['ghi']-df['dhi'])/cos(radians(df['zenith']))
    return df
    
    

def Skartevit2(df):

    if df['ghi'] >= 8 and df['zenith'] <= 85 and df['k_t'] <= 1.2:
        kt1=0.83-0.56*exp(-0.06*df['altitude'])
        kt11=0.83-0.56*exp(-0.06*df['alt+1'])
        kt111=0.83-0.56*exp(-0.06*df['alt-1'])
        if df['altitude']<=1.4:
            kd1=1.0
        if df['altitude']>1.4:
            kd1=0.07+0.046*(90-df['altitude'])/(df['altitude']+3)
        k1=0.5*(1+sin(pi*(df['k_t']-0.22)/(kt1-0.22)-pi/2))
        kt2=0.95*kt1
        k2=0.5*(1+sin(pi*(kt2-0.22)/(kt1-0.22)-pi/2))
        kd2=1-(1-kd1)*(0.11*sqrt(k2)+0.15*k2+0.74*pow(k2,2))
        kbmax=0.81**((1/sin(radians(df['altitude'])))**0.6)
        ktmax=(kbmax+(kd2*kt2)/(1-kt2))/(1+(kd2*kt2)/(1-kt2))
        kdmax=kd2*kt2*(1-ktmax)/(ktmax*(1-kt2))
        s=df['k_t']/kt1
        s1=df['k_t+1']/kt11
        s11=df['k_t-1']/kt111
        sigma=sqrt((pow(s-s11,2)+pow(s-s1,2))/2)
        if sigma<0.01:
            if df['k_t']<=0.22:
                df['k_d']=1
            if 0.22<df['k_t']<=kt2:
                df['k_d']=1-(1- kd1)*(0.11*sqrt(k1)+0.15*k1+0.74*pow(k1,2))
            if kt2<df['k_t']<=ktmax:
                df['k_d']=kd2*kt2*(1-df['k_t'])/(df['k_t']*(1-kt2))
            if df['k_t']>ktmax:
                df['k_d']=1-ktmax*(1-kdmax)/df['k_t']

        if sigma>=0.01:
            kx=0.56-0.32*exp(-0.06*df['altitude'])
            kl=(df['k_t']-0.014)/(kx-0.14)
            kr=(df['k_t']-kx)/0.71
            if df['k_t']<0.14:
                delta=0
            if 0.14<=df['k_t']<=kx:
                delta=-3*pow(kl,2)*(1-kl)*pow(sigma,1.3)
            if kx<df['k_t']<=kx+0.71:
                delta=3*kr*pow((1-kr),2)*pow(sigma,0.6)
            if df['k_t']>kx+0.71:
                delta=0

            if df['k_t']<=0.22:
                df['k_d']=1+delta
            if 0.22<df['k_t']<=kt2:
                df['k_d']=1-(1- kd1)*(0.11*sqrt(abs(k1))+0.15+k1+0.74*pow(k1,2))+delta
            if kt2<df['k_t']<=ktmax:
                df['k_d']=kd2*kt2*(1-df['k_t'])/(df['k_t']*(1-kt2))+delta
            if df['k_t']>ktmax:
                df['k_d']=1-ktmax*(1-kdmax)/df['k_t']+delta
            
        df['dhi'] = abs(df['k_d'])*df['ghi']
        df['dni'] = (df['ghi']-df['dhi'])/cos(radians(df['zenith']))
    
    return df



def Engerer2(df):
    S_cost = 1367  
    C=0.042336
    b0=-3.7912
    b1=7.5479
    b2=-0.010036
    b3=0.0031480
    b4=-5.3146
    b5=1.7073
    if df['ghi'] >= 8 and df['zenith'] <= 85 and df['k_t'] <= 1.2:
        df['G_0'] = S_cost*(1 + 0.03344*cos(radians(360*(df['doy'])/365.25)))*cos(radians(df['zenith']))
        ktc=df['G_c']/df['G_0']
        deltak=ktc-df['k_t']
        
        #df['k_d']=0.042336+(1-0.042336)/(1+exp(-3.7912+7.5479*df['k_t']-0.010036*df['AST']+0.0031480*df['zenith']-5.3146+deltak))
        df['k_d']=C+(1-C)/(1+exp(b0+b1*df['k_t']+b2*df['AST']+b3*df['zenith']+b4*deltak))
        df['dhi'] = df['k_d']*df['ghi']
        df['dni'] = (df['ghi']-df['dhi'])/cos(radians(df['zenith']))
    return df


def erbs(df):
   

    if 0.22 < df['k_t'] <= 0.8:
        df['k_d'] = 0.951-0.1604*df['k_t']+4.388*pow(df['k_t'],2)-16.638*pow(df['k_t'],3)+12.336*pow(df['k_t'],4)
    elif 0 < df['k_t'] <= 0.22:
        df['k_d'] = 1-0.09*df['k_t']
    else:
        df['k_d'] = 0.165

    if df['ghi'] >= 8 and df['zenith'] <= 85 and df['k_t'] <= 1.2:
    #if df['ghi'] >= 8 and df['k_t'] <= 1.2:
        df['dhi'] = df['k_d']*df['ghi']
        df['dni'] = (df['ghi']-df['dhi'])/cos(radians(df['zenith']))
    return df


def orgil(df):

    if 0.35 <= df['k_t'] <= 0.75:
        df['k_d'] = 1.557-1.84*df['k_t']
    elif df['k_t'] < 0.35:
        df['k_d'] = 1-0.249*df['k_t']
    else:
        df['k_d'] = 0.177
    if df['ghi'] >= 8 and df['zenith'] <= 85 and df['k_t'] <= 1.2:
        df['dhi'] = df['k_d']*df['ghi']
        df['dni'] = (df['ghi']-df['dhi'])/cos(radians(df['zenith']))
    return df


def reindl(df):
   

    if 0.3 < df['k_t'] < 0.78:
        df['k_d'] = 1.45-1.67*df['k_t']
    elif df['k_t'] <= 0.3:
        df['k_d'] = 1.02-0.248*df['k_t']
    else:
        df['k_d'] = 0.147
    if df['ghi'] >= 8 and df['zenith'] <= 85 and df['k_t'] <= 1.2:
        df['dhi'] = df['k_d']*df['ghi']
        df['dni'] = (df['ghi']-df['dhi'])/cos(radians(df['zenith'])) 
    return df


def miguel(df):

    if 0.21 < df['k_t'] <= 0.76:
        df['k_d'] = 0.724+2.738*df['k_t']-8.32*pow(df['k_t'],2)+4.967*pow(df['k_t'],3)
    elif df['k_t'] <= 0.21:
        df['k_d'] = 0.0995-0.081*df['k_t']
    else:
        df['k_d'] = 0.18

    if df['ghi'] >= 8 and df['zenith'] <= 85 and df['k_t'] <= 1.2:
        df['dhi'] = df['k_d']*df['ghi']
        df['dni'] = (df['ghi']-df['dhi'])/cos(radians(df['zenith']))
    return df


def karatasou(df):

    if df['k_t'] <= 0.78:
        df['k_d'] = 0.9995-0.05*df['k_t']-2.4156*pow(df['k_t'],2)+1.4926*pow(df['k_t'],3)
    else:
        df['k_d'] = 0.2

    #if df['ghi'] >= 8 and df['zenith'] <= 85 and df['k_t'] <= 1.2:
    df['dhi'] = df['k_d']*df['ghi']
    df['dni'] = (df['ghi']-df['dhi'])/cos(radians(df['zenith']))
    if df['dni']<=0:
        df['dhi'] = df['ghi']
        df['dni'] = 0
    
    return df


def boland(df):
   

    df['k_d'] = 1/(1+exp(7.997*(df['k_t']-0.586)))

    if df['ghi'] >= 8 and df['zenith'] <= 85 and df['k_t'] <= 1.2:
        df['dhi'] = df['k_d']*df['ghi']
        df['dni'] = (df['ghi']-df['dhi'])/cos(radians(df['zenith']))
    return df

def boland1(df):

    if df['ghi'] >= 8 and df['zenith'] <= 85 and df['k_t'] <= 1.2:
        df['k_d'] = 0.952-1.041*exp(-exp(2.3-4.702*df['k_t']))
        df['dhi'] = df['k_d']*df['ghi']
        df['dni'] = (df['ghi']-df['dhi'])/cos(radians(df['zenith']))
    return df

def k_calc(df):
    df['k_b'] = df['dni']/df['dni_clear']
    df['k_d'] = df['dhi']/df['dhi_clear']
    
    if df['k_b']>1:
        df['k_b']=1
    
    if df['k_d']>=1:
        df['k_d']=1
    
    return df
    
    
def main(df,latitude,longitude,elevation,model='Karatasou'):
    slope=0
    aspect=0
    import time
    S_cost = 1367  
    df['azimuth'] = 0.0
    df['zenith'] = 0.0
    df['altitude'] = 0.0
    df['AST'] = 0.0
    df['G_0'] = 0.0
    df['k_d'] = 0.0
    df['dhi'] = 0.0
    df['dni'] = 0.0
    df['k_b'] = 0.0
    df['G_1'] = 0.0
    df['doy'] = df.index.dayofyear

    Linke={1:3.5,2:4.3,3:4,4:4.2,5:4.6,6:4.6,7:4.4,8:4.5,9:4.3,10:4,11:4.4,12:4.4}

    loc=pvlib.location.Location(latitude, longitude, tz='UTC', altitude=elevation, name=None)
    pres=pvlib.atmosphere.alt2pres(loc.altitude)
    df['azimuth'] = (loc.get_solarposition(df.index, pressure=pres, temperature=12)['azimuth']-180).values
    df['altitude']= (loc.get_solarposition(df.index, pressure=pres, temperature=12)['elevation']).values
    df['zenith']=(loc.get_solarposition(df.index, pressure=pres, temperature=12)['zenith']).values
    df['AST']=(pvlib.solarposition.ephemeris(df.index, latitude, longitude, pressure=pres, temperature=12)['solar_time']).values
    df['airmass_relative']=pvlib.atmosphere.get_relative_airmass(df['zenith'], model='kastenyoung1989')
    df['m']=(pvlib.atmosphere.get_absolute_airmass(df['airmass_relative'], pressure=pres))
    df['k_t'] = pvlib.irradiance.disc(df['ghi'], df['zenith'], df.index, pressure=101325)['kt']
    clear=loc.get_clearsky(df.index,model='ineichen')
    df['dni_clear'] = clear['dni']
    df['dhi_clear'] = clear['dhi']
    df['G_c']=clear['ghi']
   


    if model=='Erbs':
        df = df.apply(erbs,axis=1)
        df=df.apply(k_calc,axis=1)
        
    if model=='Boland':
        df=df.apply(boland,axis=1)
        df=df.apply(k_calc,axis=1)
        
    if model=='Orgil':
        df=df.apply(orgil,axis=1)
        df=df.apply(k_calc,axis=1)

    if model=='Karatasou':
        df=df.apply(karatasou,axis=1)
        df=df.apply(k_calc,axis=1)

    if model=='Reindl':
        df=df.apply(reindl,axis=1)
        df=df.apply(k_calc,axis=1)


    if model=='Ruiz':
        df=df.apply(ruiz,axis=1)
        df=df.apply(k_calc,axis=1)

    if model=='Skartevit1':
        df=df.apply(Skartevit11,axis=1)
        df=df.apply(k_calc,axis=1)
        

    if model=='Engerer2':
        df=df.apply(Engerer2,axis=1)
        kde=max(0.1-df['G_c']/df['ghi'])
        plt.plot(df.index,df['k_d'])
        df=df.apply(k_calc,axis=1)      
          
    if model=='Skartevit2':
        df['alt+1']=df['altitude'].shift(1)
        df['alt-1']=df['altitude'].shift(-1)
        df['k_t+1']=df['k_t'].shift(1)
        df['k_t-1']=df['k_t'].shift(-1)
        df=df.apply(Skartevit2,axis=1)
        df=df.apply(k_calc,axis=1)        

    total_irrad=pvlib.irradiance.get_total_irradiance(slope,aspect,df.zenith,df.azimuth,df.dni,df.ghi,df.dhi)
    return df

if __name__ == "__main__":
    import sys
    main()

