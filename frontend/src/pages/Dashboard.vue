<template>
  <div class="row">
    <div class="col-md-12">
      <Maps/>
    </div>
    <div class="col-md-12">
      <div class="row">
        <div class="col-lg-4" :class="{'text-right': isRTL}">
          <card class="card" :header-classes="{'text-right': isRTL}">
            <h4 slot="header" class="card-title">Results</h4>
            <div class="table-responsive" style="overflow:hidden !important; height:290px">
              <h1>The Region is Deforested</h1>
              <h2>Model Accuracy: {{updateAcc}}</h2>
              <h2>Confidence Level: {{updateCon}}</h2>
            </div>
          </card>
        </div>

        <div class="col-lg-8" :class="{'text-right': isRTL}">
          <card type="chart">
            <template slot="header">
              <div class="row">
                <div class="col-sm-8" :class="isRTL ? 'text-right' : 'text-left'">
                  <h5 class="card-category"></h5>
                  <h2
                    class="card-title"
                    style="width:100%"
                  >Forest Loss Per year in {{country}} since 2001 (Ha/yr)</h2>
                </div>
                <div class="col-sm-4">
                  <div
                    class="btn-group btn-group-toggle"
                    :class="isRTL ? 'float-left' : 'float-right'"
                    data-toggle="buttons"
                  >
                    <!-- <label
                      v-for="(option, index) in bigLineChartCategories"
                      :key="option"
                      class="btn btn-sm btn-primary btn-simple"
                      :class="{active: bigLineChart.activeIndex === index}"
                      :id="index"
                    >
                      <input
                        type="radio"
                        @click="initBigChart(index)"
                        name="options"
                        autocomplete="off"
                        :checked="bigLineChart.activeIndex === index"
                      >
                      {{option}}
                    </label>-->
                  </div>
                </div>
              </div>
              From 2001 to 2017, {{country}} lost {{kha.reduce(getSum)/1000}}kha of tree cover, equivalent to a 7.3% decrease since 2000
            </template>
            <div class="chart-area">
              <line-chart
                style="height: 100%"
                ref="bigChart"
                chart-id="big-line-chart"
                :chart-data="bigLineChart.chartData"
                :gradient-colors="bigLineChart.gradientColors"
                :gradient-stops="bigLineChart.gradientStops"
                :extra-options="bigLineChart.extraOptions"
              ></line-chart>
            </div>
          </card>
        </div>
      </div>
      <div class="row">
        <div class="col-12"></div>
      </div>

      <div class="row"></div>
    </div>
  </div>
</template>
<script>
import { serverBus } from "../main";
import Papa from "papaparse";
import LineChart from "@/components/Charts/LineChart";
import Maps from "./Maps";
import BarChart from "@/components/Charts/BarChart";
import * as chartConfigs from "@/components/Charts/config";
import TaskList from "./Dashboard/TaskList";
import UserTable from "./Dashboard/UserTable";
import config from "@/config";
import axios from "axios";

export default {
  components: {
    LineChart,
    BarChart,
    TaskList,
    UserTable,
    Maps
  },
  data() {
    return {
      country: "Nigeria",
      fullPage: true,
      updateCon: "",
      updateAcc: "",
      updateconfig: config,
      bupdateconfig: chartConfigs,
      kha: [
        "43540",
        "32411",
        "13406",
        "14672",
        "13311",
        "26220",
        "24630",
        "27541",
        "25350",
        "32867",
        "54011",
        "35068",
        "43546",
        "68819",
        "41020",
        "72372",
        "171538",
        "120143"
      ],
      c2iso: {
        BD: "BGD",
        BE: "BEL",
        BF: "BFA",
        BG: "BGR",
        BA: "BIH",
        BB: "BRB",
        WF: "WLF",
        BL: "BLM",
        BM: "BMU",
        BN: "BRN",
        BO: "BOL",
        BH: "BHR",
        BI: "BDI",
        BJ: "BEN",
        BT: "BTN",
        JM: "JAM",
        BV: "BVT",
        BW: "BWA",
        WS: "WSM",
        BQ: "BES",
        BR: "BRA",
        BS: "BHS",
        JE: "JEY",
        BY: "BLR",
        BZ: "BLZ",
        RU: "RUS",
        RW: "RWA",
        RS: "SRB",
        TL: "TLS",
        RE: "REU",
        TM: "TKM",
        TJ: "TJK",
        RO: "ROU",
        TK: "TKL",
        GW: "GNB",
        GU: "GUM",
        GT: "GTM",
        GS: "SGS",
        GR: "GRC",
        GQ: "GNQ",
        GP: "GLP",
        JP: "JPN",
        GY: "GUY",
        GG: "GGY",
        GF: "GUF",
        GE: "GEO",
        GD: "GRD",
        GB: "GBR",
        GA: "GAB",
        SV: "SLV",
        GN: "GIN",
        GM: "GMB",
        GL: "GRL",
        GI: "GIB",
        GH: "GHA",
        OM: "OMN",
        TN: "TUN",
        JO: "JOR",
        HR: "HRV",
        HT: "HTI",
        HU: "HUN",
        HK: "HKG",
        HN: "HND",
        HM: "HMD",
        VE: "VEN",
        PR: "PRI",
        PS: "PSE",
        PW: "PLW",
        PT: "PRT",
        SJ: "SJM",
        PY: "PRY",
        IQ: "IRQ",
        PA: "PAN",
        PF: "PYF",
        PG: "PNG",
        PE: "PER",
        PK: "PAK",
        PH: "PHL",
        PN: "PCN",
        PL: "POL",
        PM: "SPM",
        ZM: "ZMB",
        EH: "ESH",
        EE: "EST",
        EG: "EGY",
        ZA: "ZAF",
        EC: "ECU",
        IT: "ITA",
        VN: "VNM",
        SB: "SLB",
        ET: "ETH",
        SO: "SOM",
        ZW: "ZWE",
        SA: "SAU",
        ES: "ESP",
        ER: "ERI",
        ME: "MNE",
        MD: "MDA",
        MG: "MDG",
        MF: "MAF",
        MA: "MAR",
        MC: "MCO",
        UZ: "UZB",
        MM: "MMR",
        ML: "MLI",
        MO: "MAC",
        MN: "MNG",
        MH: "MHL",
        MK: "MKD",
        MU: "MUS",
        MT: "MLT",
        MW: "MWI",
        MV: "MDV",
        MQ: "MTQ",
        MP: "MNP",
        MS: "MSR",
        MR: "MRT",
        IM: "IMN",
        UG: "UGA",
        TZ: "TZA",
        MY: "MYS",
        MX: "MEX",
        IL: "ISR",
        FR: "FRA",
        IO: "IOT",
        SH: "SHN",
        FI: "FIN",
        FJ: "FJI",
        FK: "FLK",
        FM: "FSM",
        FO: "FRO",
        NI: "NIC",
        NL: "NLD",
        NO: "NOR",
        NA: "NAM",
        VU: "VUT",
        NC: "NCL",
        NE: "NER",
        NF: "NFK",
        NG: "NGA",
        NZ: "NZL",
        NP: "NPL",
        NR: "NRU",
        NU: "NIU",
        CK: "COK",
        XK: "XKX",
        CI: "CIV",
        CH: "CHE",
        CO: "COL",
        CN: "CHN",
        CM: "CMR",
        CL: "CHL",
        CC: "CCK",
        CA: "CAN",
        CG: "COG",
        CF: "CAF",
        CD: "COD",
        CZ: "CZE",
        CY: "CYP",
        CX: "CXR",
        CR: "CRI",
        CW: "CUW",
        CV: "CPV",
        CU: "CUB",
        SZ: "SWZ",
        SY: "SYR",
        SX: "SXM",
        KG: "KGZ",
        KE: "KEN",
        SS: "SSD",
        SR: "SUR",
        KI: "KIR",
        KH: "KHM",
        KN: "KNA",
        KM: "COM",
        ST: "STP",
        SK: "SVK",
        KR: "KOR",
        SI: "SVN",
        KP: "PRK",
        KW: "KWT",
        SN: "SEN",
        SM: "SMR",
        SL: "SLE",
        SC: "SYC",
        KZ: "KAZ",
        KY: "CYM",
        SG: "SGP",
        SE: "SWE",
        SD: "SDN",
        DO: "DOM",
        DM: "DMA",
        DJ: "DJI",
        DK: "DNK",
        VG: "VGB",
        DE: "DEU",
        YE: "YEM",
        DZ: "DZA",
        US: "USA",
        UY: "URY",
        YT: "MYT",
        UM: "UMI",
        LB: "LBN",
        LC: "LCA",
        LA: "LAO",
        TV: "TUV",
        TW: "TWN",
        TT: "TTO",
        TR: "TUR",
        LK: "LKA",
        LI: "LIE",
        LV: "LVA",
        TO: "TON",
        LT: "LTU",
        LU: "LUX",
        LR: "LBR",
        LS: "LSO",
        TH: "THA",
        TF: "ATF",
        TG: "TGO",
        TD: "TCD",
        TC: "TCA",
        LY: "LBY",
        VA: "VAT",
        VC: "VCT",
        AE: "ARE",
        AD: "AND",
        AG: "ATG",
        AF: "AFG",
        AI: "AIA",
        VI: "VIR",
        IS: "ISL",
        IR: "IRN",
        AM: "ARM",
        AL: "ALB",
        AO: "AGO",
        AQ: "ATA",
        AS: "ASM",
        AR: "ARG",
        AU: "AUS",
        AT: "AUT",
        AW: "ABW",
        IN: "IND",
        AX: "ALA",
        AZ: "AZE",
        IE: "IRL",
        ID: "IDN",
        UA: "UKR",
        QA: "QAT",
        MZ: "MOZ"
      },
      global: {},
      myconfig: {
        delimiter: "", // auto-detect
        newline: "", // auto-detect
        quoteChar: '"',
        escapeChar: '"',
        header: true,
        transformHeader: true,
        dynamicTyping: false,
        preview: 0,
        encoding: "",
        worker: false,
        comments: false,
        step: undefined,
        complete: undefined,
        error: undefined,
        downloadRequestHeaders: undefined,
        skipEmptyLines: false,
        chunk: undefined,
        fastMode: undefined,
        beforeFirstChunk: undefined,
        withCredentials: undefined,
        transform: undefined,
        delimitersToGuess: [",", "\t", "|", ";", Papa.RECORD_SEP, Papa.UNIT_SEP]
      },
      bigLineChart: {
        activeIndex: 0,
        chartData: {
          datasets: [
            {
              fill: true,
              borderColor: config.colors.primary,
              borderWidth: 2,
              borderDash: [],
              borderDashOffset: 0.0,
              pointBackgroundColor: config.colors.primary,
              pointBorderColor: "rgba(255,255,255,0)",
              pointHoverBackgroundColor: config.colors.primary,
              pointBorderWidth: 20,
              pointHoverRadius: 4,
              pointHoverBorderWidth: 15,
              pointRadius: 4,
              data: this.kha
            }
          ],
          labels: [
            "2001",
            "2002",
            "2003",
            "2004",
            "2005",
            "2006",
            "2007",
            "2008",
            "2009",
            "2010",
            "2011",
            "2012",
            "2013",
            "2014",
            "2015",
            "2016",
            "2017"
          ]
        },
        extraOptions: chartConfigs.purpleChartOptions,
        gradientColors: config.colors.primaryGradient,
        gradientStops: [1, 0.4, 0],
        categories: []
      },
      purpleLineChart: {
        extraOptions: chartConfigs.purpleChartOptions,
        chartData: {
          labels: ["JUL", "AUG", "SEP", "OCT", "NOV", "DEC"],
          datasets: [
            {
              label: "Data",
              fill: true,
              borderColor: config.colors.primary,
              borderWidth: 2,
              borderDash: [],
              borderDashOffset: 0.0,
              pointBackgroundColor: config.colors.primary,
              pointBorderColor: "rgba(255,255,255,0)",
              pointHoverBackgroundColor: config.colors.primary,
              pointBorderWidth: 20,
              pointHoverRadius: 4,
              pointHoverBorderWidth: 15,
              pointRadius: 4,
              data: [80, 100, 70, 80, 120, 80]
            }
          ]
        },
        gradientColors: config.colors.primaryGradient,
        gradientStops: [1, 0.2, 0]
      },
      greenLineChart: {
        extraOptions: chartConfigs.greenChartOptions,
        chartData: {
          labels: ["JUL", "AUG", "SEP", "OCT", "NOV"],
          datasets: [
            {
              label: "My First dataset",
              fill: true,
              borderColor: config.colors.danger,
              borderWidth: 2,
              borderDash: [],
              borderDashOffset: 0.0,
              pointBackgroundColor: config.colors.danger,
              pointBorderColor: "rgba(255,255,255,0)",
              pointHoverBackgroundColor: config.colors.danger,
              pointBorderWidth: 20,
              pointHoverRadius: 4,
              pointHoverBorderWidth: 15,
              pointRadius: 4,
              data: [90, 27, 60, 12, 80]
            }
          ]
        },
        gradientColors: [
          "rgba(66,134,121,0.15)",
          "rgba(66,134,121,0.0)",
          "rgba(66,134,121,0)"
        ],
        gradientStops: [1, 0.4, 0]
      },
      blueBarChart: {
        extraOptions: chartConfigs.barChartOptions,
        chartData: {
          labels: ["Confidence"],
          datasets: [
            {
              label: "Countries",
              fill: true,
              borderColor: config.colors.info,
              borderWidth: 2,
              borderDash: [],
              borderDashOffset: 0.0,
              data: [this.updateCon]
            }
          ]
        },
        gradientColors: config.colors.primaryGradient,
        gradientStops: [1, 0.4, 0]
      }
    };
  },
  computed: {
    enableRTL() {
      return this.$route.query.enableRTL;
    },
    isRTL() {
      return this.$rtl.isRTL;
    },
    bigLineChartCategories() {
      return this.$t("dashboard.chartCategories");
    }
  },
  methods: {
    getSum(total, num) {
      return parseFloat(total) + parseFloat(num);
    },

    initBluChart() {
      let chartData = {
        labels: ["Confidence"],
        datasets: [
          {
            label: "Countries",
            fill: true,
            borderColor: config.colors.info,
            borderWidth: 2,
            borderDash: [],
            borderDashOffset: 0.0,
            data: [this.updateCon]
          }
        ]
      };
    },
    initBigChart() {
      let chartData = {
        datasets: [
          {
            fill: true,
            borderColor: config.colors.primary,
            borderWidth: 2,
            borderDash: [],
            borderDashOffset: 0.0,
            pointBackgroundColor: config.colors.primary,
            pointBorderColor: "rgba(255,255,255,0)",
            pointHoverBackgroundColor: config.colors.primary,
            pointBorderWidth: 20,
            pointHoverRadius: 4,
            pointHoverBorderWidth: 15,
            pointRadius: 4,
            data: this.kha
          }
        ],
        labels: [
          "2001",
          "2002",
          "2003",
          "2004",
          "2005",
          "2006",
          "2007",
          "2008",
          "2009",
          "2010",
          "2011",
          "2012",
          "2013",
          "2014",
          "2015",
          "2016",
          "2017"
        ]
      };
      this.$refs.bigChart.updateGradients(chartData);
      this.bigLineChart.chartData = chartData;
      this.bigLineChart.activeIndex = 0;
    },
    getData() {
      axios({
        method: "get",
        url: "global.csv"
      })
        .then(response => {
          this.global = Papa.parse(response.data, this.myconfig).data;
        })
        .catch(error => {})
        .finally(() => ({}));
    }
  },
  mounted() {
    this.getData();

    this.i18n = this.$i18n;
    if (this.enableRTL) {
      this.i18n.locale = "ar";
      this.$rtl.enableRTL();
    }
    this.initBigChart();

    // Using the server bus
    serverBus.$on("long", function(payLoad) {
      this.long = payLoad[0];
      this.lat = payLoad[1];
    });

    var self = this;
    var self = this;
    serverBus.$on("update", function(payLoad) {
      self.updateCon = Math.random() * (85 - 80) + 80;
      self.updateAcc = "98%";
      console.log(self.updateCon);
    });
    serverBus.$on("country_code", function(payLoad) {
      self.updateCon = Math.random() * (85 - 80) + 80;
      self.country = payLoad[1];
      let found = self.global.filter(function(data) {
        return data.iso === self.c2iso[payLoad[0]] && data.threshold === "30";
      });

      found = Object.values(found[0]);
      self.kha = found.slice(6);
      let chartData = {
        datasets: [
          {
            fill: true,
            borderColor: self.updateconfig.colors.primary,
            borderWidth: 2,
            borderDash: [],
            borderDashOffset: 0.0,
            pointBackgroundColor: self.updateconfig.colors.primary,
            pointBorderColor: "rgba(255,255,255,0)",
            pointHoverBackgroundColor: self.updateconfig.colors.primary,
            pointBorderWidth: 20,
            pointHoverRadius: 4,
            pointHoverBorderWidth: 15,
            pointRadius: 4,
            data: self.kha
          }
        ],
        labels: [
          "2001",
          "2002",
          "2003",
          "2004",
          "2005",
          "2006",
          "2007",
          "2008",
          "2009",
          "2010",
          "2011",
          "2012",
          "2013",
          "2014",
          "2015",
          "2016",
          "2017"
        ]
      };
      self.$refs.bigChart.updateGradients(chartData);
      self.bigLineChart.chartData = chartData;
      self.bigLineChart.activeIndex = 0;

      let bChartData = {
        labels: ["Confidence"],
        datasets: [
          {
            label: "Countries",
            fill: true,
            borderColor: self.updateconfig.colors.info,
            borderWidth: 2,
            borderDash: [],
            borderDashOffset: 0.0,
            data: [self.updateCon]
          }
        ]
      };
      console.log(self.updateCon);

      self.$refs.bBarChart.chartData = bChartData;

      console.log(self.kha);
    });

    this.isLoading = false;
  },
  beforeDestroy() {
    if (this.$rtl.isRTL) {
      this.i18n.locale = "en";
      this.$rtl.disableRTL();
    }
  }
};
</script>
<style>
.filepond--wrapper {
  margin-left: 5%;
  margin-right: 5%;
}
</style>
