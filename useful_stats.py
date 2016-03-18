


'''
CONTENTS:


'''

#confidence intervals
'''
confidence intervals for location of the mean
* mu is in (-1.96 *sigma/sqrt(n) + x_bar, 1.96 *sigma/sqrt(n) + x_bar) 
with 95% confidence
* If we select 100 samples and compute confidence intervals, 
95 of those will contain the population mean mu
'''

# if we have sigma and 95% confidence, we use 
x_bar = np.mean(X)
upper, lower = -1.96 *sigma/sqrt(n) + x_bar, 1.96 *sigma/sqrt(n) + x_bar 
# in the case of alpha = 0.05, this gives us _alpha_2 = 1.96
z_alpha_2 = stats.norm.isf(alpha/2)
# or,
# The 68% confidence interval for the mean of N draws from a 
# normal distribution with mean mu and std deviation sigma is
stats.norm.interval(0.68, loc=mu, scale=sigma/sqrt(N))
# example: for mu = 5
# >>> stats.norm.interval(0.68, loc=mu, scale=sigma/sqrt(N))
# (4.2044336934321977, 5.7955663065678031)
# >>> stats.norm.interval(0.95, loc=mu, scale=sigma/sqrt(N))
# (3.4320288123679568, 6.5679711876320432)


# if we don't have sigma, use s = var(X)
# t = (x_bar - mu ) / (s/sqrt(n)) 
#INCLUDE DEGREES OF FREEDOMS, deg = n - 1
z_alpha_2 = stats.t.isf(alpha/2 , deg)
>>> N = 20
>>> stats.t.interval(0.95, N-1, loc=mu, scale=sigma/sqrt(N))
(1.2558847486407245, 8.7441152513592755)
>>> stats.norm.interval(0.95, loc=mu, scale=sigma/sqrt(N))
(1.4939098376936739, 8.5060901623063252)


# bayesian approach to confidence intervals
# alpha is the confidence level
mean, var, std = scipy.stats.bayes_mvs(data, alpha=0.95)



# bootstrap CI
import scikits.bootstrap as bootstrap  
# compute 95% confidence intervals around the mean  
CIs = bootstrap.ci(data=treatment1, statfunction=scipy.mean, alpha = .05, n_samples=20000)  
  
print "Bootstrapped 95% confidence intervals\nLow:", CIs[0], "\nHigh:", CIs[1]  
  
Bootstrapped 95% confidence intervals  
Low: 0.659028048   
High: 1.722468024  

'''
Hypothesis testing. 
If we know the population sigma: use z-test
If we don;t know population sigma: use t-test

Types of error:
*) Type I error: Rejecting the null hypothesis H0 when it is true
Eg: Determining that a treatment has an effect when in reality 
there's no difference between patients in treatment and patients
without the treatment.
alpha = .05 --> If we repeat the experiment many times,
we would be rejecting a true null hypothesis H0 5% of the time.

*)Type II error: Fail to reject a false H0, known as "beta"
Eg: Unable to identify difference bewteen 2 populations,
when there was in fact a true difference.

*) Power of a test : 1 - beta : likelihood that a test will
correctly reject a false H0. - prob of detecting a difference
when it really exists.
'''


'''
Comparing 2 means.
'''
#Paired samples: The same patient before and after treatment
stat, pval = stats.ttest_rel(a, b)

# Independent samples
# If equal variance assumed: 
stat, pval = stats.ttest_ind(a, b)

#If not, welche's t test is used instead. 
stat, pval = ttest_ind(a, b, equal_var=False)




'''
ANOVA
ANOVA is just an extension of the t-test!!!
H0: mu_1 = mu_2 = ... = mu_k
Compute the F statistic,
F = s_B**2 / s_W**2
where s_B is the weighted average of how different each mean is from the total mean,
and s_w is a weighted average of the sample variances
Both s_b and s_w are estimating the total variance sigma.
If there is no difference between classes, F ~ 1.
F ~ F dist with k -1, n-k degs of freedom 
'''
stat, pval = stats.f_oneway(sample1, sample2, sample3, ...)

'''
If we reject the null hypothesis, do all the pairwise comparisons to 
determine which means are different.
Do: Bonferroni correction. If the overall alpha we want is 0.05,
use alpha* = alpha / (k choose 2) as the significance level for 
each pairwise test
'''


# another option: use statmodels
from statsmodels.stats.multicomp import pairwise_tukeyhsd
print pairwise_tukeyhsd(Data, Group)

'''
Tukey: Create confidence intervals for all differences
of means, see if the confidence interval contains
0 or not.
It assumes independence of the observations being tested, 
as well as equal variation across observations (homoscedasticity).
Tukey's test is essentially a Student's t-test,
 except that it corrects for family-wise error-rate.

This is multicomparison. The output is like

Multiple Comparison of Means - Tukey HSD,FWER=0.05
================================================
group1 group2 meandiff   lower    upper   reject
------------------------------------------------
  0      1    -35.2153 -114.8741 44.4434  False 
  0      2     46.697   -40.4993 133.8932 False 
  0      3    -7.5709    -87.49  72.3482  False 
  1      2    81.9123    5.0289  158.7956  True 
  1      3    27.6444   -40.8751  96.164  False 
  2      3    -54.2679 -131.4209 22.8852  False 
------------------------------------------------
Does not give p values

Conclusions	The simultaneous pairwise comparisons indicate 
that the differences μ1−μ4 and μ2−μ3 are not significantly 
different from 0 (their confidence intervals include 0), 
and all the other pairs are significantly different.
see more here: 
http://jspktd.blogspot.com/2013/03/
multiple-comparison-and-tukey-hsd-or_25.html
'''

''' 
NON PARAMETRIC test
No assumptions of underlying distributions
Pros:
* just assume both dists have similar shape, not normal
* ranksinstead of # give us less sensitivity to meas errors
Cons:
* parametric tests more powerful
'''

# WILCOXON SIGNED-RANK TESTS
# means of populations that are not independent
# omparing two related samples, matched samples, 
# or repeated measurements on a single sample
# If y is not given, then the x array is considered 
# to be the differences between the two sets of measurements.
# require n > 20
stat, pval  = scipy.stats.wilcoxon(x, y=None)

# WILCOXON RANK SUM TEST
# independent samples \
# rank all obs, sum ranks in pop1 and pop 2
stat, pval = scipy.stats.ranksums(x, y)


'''
Chi squared distribution
Contingency tables
				Handedness
Gender
		Right handed	Left handed	Total
Male	43				9			52
Female	44				4			48
Total	87				13			100
'''

chi2, p, dof, ex = chi2_contingency(obs, correction=False)





