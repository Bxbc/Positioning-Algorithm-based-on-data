function f = fun(x)
data1 = cell2mat(struct2cell(load('C:\Users\BC\Desktop\mlabneed\data.mat')));
f=((x(1)-(data1(2,1)))^2 + (x(2)-data1(2,2))^2 - (x(1)-data1(2,3))^2 - (x(2)-data1(2,4))^2)^2;
end