require 'net/http'
require 'rubygems'
require 'json'
 
EMAIL = "quantum7@gmail.com"
PASSWORD = "2036334"
 
def get_stikkits(page = 1)
  response = Net::HTTP.start('api.stikkit.com') { |http|
    req = Net::HTTP::Get.new("/stikkits.json?page=#{page}")
    req.basic_auth(EMAIL, PASSWORD)
    http.request(req)
  }
  JSON.parse(response.body)
end
 
stikkits = []
page = 1
until (page_of_stikkits = get_stikkits(page)).empty?
  stikkits += page_of_stikkits
  page += 1
end
 
File.open('stikkits.yml', 'w') { |f| f.write stikkits.to_yaml }
puts "Saved #{stikkits.length} stikkits (#{stikkits.map { |s| "\"#{s['name']}\"" }.join(', ')})"
