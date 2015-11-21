import ConfigParser, logging, datetime, os

from flask import Flask, render_template, request

import mediacloud

CONFIG_FILE = 'settings.config'
basedir = os.path.dirname(os.path.realpath(__file__))

# load the settings file
config = ConfigParser.ConfigParser()
config.read(os.path.join(basedir, 'settings.config'))

# set up logging
log_file_path = os.path.join(basedir,'logs','mcserver.log')
logging.basicConfig(filename=log_file_path,level=logging.DEBUG)
logging.info("Starting the MediaCloud example Flask app!")

# clean a mediacloud api client
mc = mediacloud.api.MediaCloud( config.get('mediacloud','api_key') )

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("search-form.html")

@app.route("/search",methods=['POST'])
def search_results():
    keywords = request.form['keywords']
    startYear = request.form['startYear']
    intStartYear = int(startYear)
    startMonth = request.form["startMonth"]
    intStartMonth = int(startMonth)
    startDay = request.form["startDay"]
    intStartDay = int(startDay)
    endYear = request.form['endYear']
    intEndYear = int(endYear)
    endYear = request.form['endYear']
    endMonth = request.form["endMonth"]
    intEndMonth = int(endMonth)
    endDay = request.form["endDay"]
    intEndDay = int(endDay)
    strStartDate = str(startYear+'-'+startMonth+'-'+startDay)
    strEndDate = str(endYear+'-'+endMonth+'-'+endDay)
    now = datetime.datetime.now()
    results = mc.sentenceCount(keywords,
        solr_filter=[mc.publish_date_query( datetime.date( intStartYear, intStartMonth, intStartDay),
                                            datetime.date( intEndYear, intEndMonth, intEndDay) ),
                     'media_sets_id:1' ],split=True,split_start_date=strStartDate,split_end_date=strEndDate)
    return render_template("search-results.html",
        keywords=keywords, sentenceCount=results['count'], sentenceSplit=results['split'] )

if __name__ == "__main__":
    app.debug = True
    app.run()


#'%d' % (startYear)
