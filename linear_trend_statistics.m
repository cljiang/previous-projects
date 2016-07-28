%  1. Linear regression fitting to a time series x; 
%  2. Test the statistical significance of the linear trend;
%  details see Calculate_confidence_interval_using_t_test.pdf

clear
load Linear_trend_statistics.mat

% data consists of
% x - time series;
% year - years of x;

whos

% plot
figure(1);
plot(year,x,'b*-');
xlabel('Year');
ylabel('x');

% - (1) Is there an overlying linear trend (increasing or decreasing)? 
%       If so, is it significant?

%Solutions: 
% - (1) linear regression fit;
% - (2) test if the true slope with 95% confidence will be larger than zero;
% - (3) test if the linear trend will fall outside of the 95% confidence 
%       interval for the true mean;

% - (1) do the linear regression
p=polyfit(year,x,1);
b1=p(1); 
b0=p(2);
x_polyfit=b1*year+b0; %linear regression model

%plot 
figure(1);hold on; plot(year,x_polyfit,'k','linewidth',3);

% - (2) compute the 95% confidence interval for the true slope (Section3 in Confidence_interval.pdf)
%N_star - effective degrees of freedom in x;
%nu_slope - degrees of freedom 
[tau,N_star] = time_scale(x)
nu_slope=N_star-2

%S_epsilon - standard error of the linear regression estimate
S_epsilon=sqrt(sum((x-x_polyfit).^2)/nu_slope);

%l_xx = \sum(x_{i}-\overline{x})^{2}
l_xx=sum((year-mean(year)).^2);

%95% confidence interval for the true slope (equation5 in Confidence_interval.pdf)
%obtain t(nu_slope=?,0.025)=XXXXXX from Hartmann's one-tailed t tables (552_Notes_Tables_Chap1.pdf)
%b1_lower_95 is the lower limit of the true slope in equation5
%b1_upper_95 is the upper limit of the true slope in euqation5
t_025_slope=XXXXXX
b1_lower_95=XXXXXX
b1_upper_95=XXXXXX

%see what the estimated slope is:
b1

%plot
figure(1);hold on;plot(year,b1_lower_95*year+(b1-b1_lower_95)*year(1)+b0,'k--',year,b1_upper_95*year+(b1-b1_upper_95)*year(1)+b0,'k--','linewidth',2);

% - (3) compute the 95% confidence interval for the true mean (Section2 in Confidence_interval.pdf)
%95% confidence interval for the true mean (equation4 in Confidence_interval.pdf)
%obtain t(nu_mean=?,0.025)= from Hartmann's one-tailed t tables (552_Notes_Tables_Chap1.pdf)
%mu_lower_95 is the lower limit of the true mean in equation4
%mu_upper_95 is the upper limit of the true mean in equation4
nu_mean=N_star-1
t_025_mean=XXXXXX
mu_lower_95=XXXXXX 
mu_upper_95=XXXXXX 

%plot
figure(1);hold on;
plot(year,mu_lower_95*ones(1,length(year)),'r',year,mu_upper_95*ones(1,length(year)),'r','linewidth',2);

%the linear trend is significant?
%compare this value
mu_upper_95-mu_lower_95

%with these values.
b1_lower_95*(year(length(year))-year(1))
b1*(year(length(year))-year(1))
b1_upper_95*(year(length(year))-year(1))

