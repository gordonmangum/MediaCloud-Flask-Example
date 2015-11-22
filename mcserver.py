import ConfigParser, logging, datetime, os, json

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
    # attempt at input validation to add leading zero
    #intStartMonth = "%02d" % intStartMonth
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

    logging.info('Data goes here!')
    data = results['split']
    #for key in data:
        #logging.info(key)
    # results must be cleaned up to work in highcharts
    dates = data.keys()
    dates_formatted = []
    for s in dates:
        s = str(s)
        s = s[0:10]
        if len(s) == 10:
            dates_formatted.append(s)
        #logging.info(s)
    logging.info(dates_formatted)

    values = data.values()
    values_formatted = []
    for t in values:
        try:
            t = int(t)
            values_formatted.append(t)
        except ValueError:
            logging.info("Removed non-integer from sentence count")

    return render_template("search-results.html",
        keywords=keywords, sentenceCount=results['count'], sentenceSplit=results['split'], splitDate=dates_formatted, values=values_formatted )


        #print key

    #for key, value in parsed_json.items():
        #splitDate = key
        #splitNum = value
        #return render_template("search-results.html", splitDate=splitDate, splitNum=splitNum)

if __name__ == "__main__":
    app.debug = True
    app.run()


#'%d' % (startYear)
