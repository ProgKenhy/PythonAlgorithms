#pragma GCC target ("arch=sandybridge")
#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>

using namespace std;


long long fast_search(vector <long long> arr) {
	long long summa = LLONG_MIN;
	long long temp = 0;
	for (long long i = 0; i < arr.size(); i++)
	{
		temp += arr[i];
		summa = max(summa, temp);
		if (temp < 0) temp = 0;
	}
	return summa;
}



int main() {
	ios::sync_with_stdio(0);
	cin.tie(0);
	long long n;
	cin >> n;
	vector <long long> arr(n);
	for (long long i = 0; i < n; i++) {
		cin >> arr[i];
	}
	cout << fast_search(arr);

	return 0;
}
