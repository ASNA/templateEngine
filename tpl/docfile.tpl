<table>

<tr><td>DB Name</td><td>{{ DBName }}</td></tr>
<tr><td>Library</td><td>{{ Library }}</td></tr>
<tr><td>File</td><td>{{ FileName }}</td></tr>
<tr><td>File alias</td><td>{{ FileAlias }}</td></tr>
<tr><td>Format</td><td>{{ Format }}</td></tr>
<tr><td>Type</td><td>{{ Type }}</td></tr>
<tr><td>Base file</td><td>{{ BaseFile }}</td></tr>
<tr><td>Description</td><td>{{ FileDescription }}</td></tr>
<tr><td>Record length</td><td>{{ RecordLength }}</td></tr>
<tr><td>Key length</td><td>{{ KeyLength }}</td></tr>
<tr><td>Key fields</td>
<td>
    {{ KeyFields | join(', ', attribute='Name') }}
</td>
</table>


<table>
<tr>
    <td>Field</td>
    <td>Type</td>
    <td>Length</td>
    <td>Decimals</td>
    <td>Description</td>
</tr>
{% for field in Fields %}
<tr>
    <td>{{ field.Name }}</td>
    <td>{{ field.Type }}</td>
    <td>{{ field.Length}}</td>
    <td>{{ field.Decimals}}</td>
    <td>{{ field.Description}}</td>
</tr>
{% endfor %}
</table>