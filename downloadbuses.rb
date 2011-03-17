require "rexml/document"
require "rexml/formatters/pretty"
require "net/http"
require "rubygems"
require "sqlite3"

$db = SQLite3::Database.new( "buses.db" )

$db.execute("create table stops (stopcode INTEGER PRIMARY KEY,name TEXT,x double,y double)")
$db.execute("create table services (stopcode INTEGER, service INTEGER)")
$db.execute("create table points (service INTEGER,chain INTEGER,x double, y double)")
$seenStops = {}


def downloadService(service)
    resource = Net::HTTP.new("mybustracker.co.uk",80)
    
    puts "Downloading service #{service}... "

    headers,data = resource.get('/getServicePoints.php?serviceMnemo='+service)
    doc = REXML::Document.new data

    print headers

    doc.elements.each("map/points/point") { |point|
       chain=point.elements['num_chainage'].text
       xloc=point.elements['x'].text
       yloc=point.elements['y'].text

       $db.execute("insert into points (service,chain,x,y) values (?,?,?,?)",service,chain,xloc,yloc)
       puts "Point #{chain},#{xloc},#{yloc}"
    }

    doc.elements.each("map/markers/busStop") { |element|
       name=element.elements['nom'].text
       code=element.elements['sms'].text
       xloc=element.elements['x'].text
       yloc=element.elements['y'].text

       if $seenStops.has_key?(code) == false
          $db.execute("insert into stops (stopcode,name,x,y) values (?,?,?,?)",code,name,xloc,yloc)
          $seenStops[code]=true
          puts "Service has stop #{name},#{code},#{xloc},#{yloc}"

       end

       #puts "--------\n#{name},#{code},#{xloc},#{yloc}" 

       element.elements['services'].each { |service|
          visitingservice=service.elements['mnemo'].text
          $db.execute("insert into services (stopcode,service) values (?,?)",code,visitingservice)
       }
   }
end

#(16..18).each { |i|
(1..100).each { |i|
   downloadService( i.to_s() )
   sleep 5
 }

