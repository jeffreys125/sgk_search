<!DOCTYPE html>
<html lang="zh-Hans">
<head>
	<meta charset="utf-8">
	<title>搜索结果</title>
	<style>
		#show_result
		{
			margin: 0 auto;
			width: 480px;
			text-align: left;
			border-collapse: collapse;
		}
		#show_result caption
		{
			font-size: 30px;
			margin: 10px;
		}
		#show_result th
		{
			font-weight: normal;
			padding: 8px;
			background: #b9c9fe;
			border-top: 4px solid #aabcfe;
			border-bottom: 1px solid #fff;
			color: #039;
		}
		#show_result td
		{
			padding: 8px;
			background: #e8edff; 
			border-bottom: 1px solid #fff;
			color: #669;
			border-top: 1px solid transparent;
		}
		#show_result tr:hover td
		{
			background: #d0dafd;
			color: #339;
		}
	</style>
</head>
<body>

<table id="show_result">
	<caption>xxxxxcaptionxxxxx</caption>
	<thead>
		<tr>
			<th>col1</th>
			<th>col2</th>
			<th>col3</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>val1</td>
			<td>val2</td>
			<td>val3</td>
		</tr>
		<tr>
			<td>val1</td>
			<td>val2</td>
			<td>val3</td>
		</tr>
	</tbody>
</table>

<script>
var table = document.getElementById('show_result'),
    thead = table.getElementsByTagName('thead')[0],
    tbody = table.getElementsByTagName('tbody')[0]

/////json/////

thead_html = '<tr><th>' + data[0].join('</th><th>') + '</th></tr>'
thead.innerHTML = thead_html

tbody_html = ''
data[1].forEach(function(line){
	tbody_html += '<tr><td>' + line.join('</td><td>') + '</td></tr>'
})
tbody.innerHTML = tbody_html

</script>
</body>
</html>