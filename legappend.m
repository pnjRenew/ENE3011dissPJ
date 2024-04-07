
%%
% <https://www.mathworks.com/matlabcentral/fileexchange/authors/15007
% Jiro>'s pick this week is
% <https://www.mathworks.com/matlabcentral/fileexchange/47228-legappend |legappend|>
% by <https://www.mathworks.com/matlabcentral/fileexchange/authors/225623
% Chad Greene>.
%
% Chad is no stranger to MATLAB Central. He has
% <https://www.mathworks.com/matlabcentral/fileexchange/index?term=authorid%3A225623
% over 50 File Exchange entries>, and two of his entries have been
% highlighted
% (<https://blogs.mathworks.com/pick/2012/07/27/1000-unit-converters-at-your-fingertips/
% unit converters> and
% <https://blogs.mathworks.com/pick/2013/07/19/clear-everything/ ccc>) in
% Pick of the Week. His entries are well-written, and like this one, many
% of his entries have
% <https://www.mathworks.com/help/matlab/matlab_prog/publishing-matlab-code.html
% published example files>.
%
% Many of you may know that the command
% <https://www.mathworks.com/help/matlab/ref/legend.html |legend|> creates
% one legend per axes.

t = 0:.1:10;
x1 = sin(t);
x2 = cos(t);
plot(t,x1,t,x2)
legend('Sine','Cosine')

%%
% Let's say that you wanted to add another line to this plot.

x3 = sin(t).*cos(t);
hold on
plot(t,x3,'--r')

%%
% To add this entry to the legend, you would re-run the |legend| command
% with the three entries.

legend('Sine','Cosine','Sine*Cosine')

%%
% Chad's |legappend| allows you to append new entries to an existing
% legend. This means that you can simply call it along with the new lines
% you create.

% New figure
figure;
plot(t,x1,t,x2)
legend('Sine','Cosine')

% Add another line
hold on
plot(t,x3,'--r')

% Append a new legend item
legappend('Sine*Cosine')

%%
% Great! You can also delete the last legend entry with the following
% command.
%
%   legappend('')
%
% If you want to see more examples, check out his published
% <https://www.mathworks.com/matlabcentral/fileexchange/47228-legappend/content/legappend/html/legappend_demo.html
% example>.
%
% Chad explains that |legappend| simply deletes the current legend and
% recreates the updated legend. This is a good example of how you can take
% a normal mode of operation and tweak it in order to adapt it to your
% needs.
%
% Give it a try and let us know what you think
% <https://blogs.mathworks.com/pick/?p=5452#respond here> or leave a
% <https://www.mathworks.com/matlabcentral/fileexchange/47228-legappend#comments
% comment> for Chad.


%%
% _Copyright 2014 The MathWorks, Inc._