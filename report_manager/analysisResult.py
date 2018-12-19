import report_manager.analyses.basicAnalysis as analyses
from report_manager.plots import basicFigures as figure
import itertools


class AnalysisResult:
    def __init__(self, identifier, analysis_type, args, data, result=None):
        self._identifier = identifier
        self._analysis_type = analysis_type
        self._args = args
        self._data = data
        self._result = result
        if self._result is None:
            self.generate_result()

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        self._identifier = identifier

    @property
    def analysis_type(self):
        return self._analysis_type

    @analysis_type.setter
    def identifier(self, analysis_type):
        self._analysis_type = analysis_type
    
    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, args):
        self._args = args

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, result):
        self._result = result


    def generate_result(self):
        result, args = self.get_analysis_result()
        self.result = result
        self.args = args

    def get_analysis_result(self):
        result = {}
        args = self.args
        if self.analysis_type == "pca":
            components = 2
            if "components" in args:
                components = args["components"]
            result, args = analyses.runPCA(self.data, components)
        elif self.analysis_type  == "tsne":
            components = 2
            perplexity = 40
            n_iter = 1000
            init='pca'
            if "components" in args:
                components = args["components"]
            if "perplexity" in args:
                perplexity = args["perplexity"]
            if "n_iter" in args:
                n_iter = args["n_iter"]
            if "init" in args:
                init = args["init"]
            result, args = analyses.runTSNE(self.data, components=components, perplexity=perplexity, n_iter=n_iter, init=init)
        elif self.analysis_type  == "umap":
            n_neighbors=10 
            min_dist=0.3
            metric='cosine'
            if "n_neighbors" in args:
                n_neighbors = args["n_neighbors"]
            if "min_dist" in args:
                min_dist = args["min_dist"]
            if "metric" in args:
                metric = args["metric"]
            if n_neighbors < self.data.shape[0]:
                result, args = analyses.runUMAP(self.data, n_neighbors=n_neighbors, min_dist=min_dist, metric=metric)
        elif self.analysis_type  == "mapper":
            n_cubes = 15
            overlap = 0.5
            n_clusters = 3
            linkage = "complete"
            affinity = "correlation"
            labels = {}
            if "labels" in args:
                labels = args["labels"]
            if "n_cubes" in args:
                n_cubes = args["n_cubes"]
            if "overlap" in args:
                overlap = args["overlap"]
            if "n_clusters" in args:
                n_clusters = args["n_clusters"]
            if "linkage" in args:
                linkage = args["linkage"]
            if "affinity" in args:
                affinity = args["affinity"]
            r, args = analyses.runMapper(self.data, n_cubes=n_cubes, overlap=overlap, 
                                            n_clusters=n_clusters, linkage=linkage, affinity=affinity)
            result[self.analysis_type] = r
        elif self.analysis_type  == 'ttest':
            alpha = 0.05
            if "alpha" in args:
                alpha = args["alpha"]
            for pair in itertools.combinations(self.data.group.unique(),2):
                ttest_result = analyses.ttest(self.data, pair[0], pair[1], alpha = 0.05)
                result[pair] = ttest_result
        elif self.analysis_type  == 'anova':
            alpha = 0.05
            if "alpha" in args:
                alpha = args["alpha"]
            anova_result = analyses.anova(self.data, alpha = 0.05)
            result[self.analysis_type] = anova_result
        elif self.analysis_type  == "correlation":
            alpha = 0.05
            method = 'pearson'
            correction = ('fdr', 'indep')
            if "alpha" in args:
                alpha = args["args"]
            if "method" in args:
                method = args["method"]
            if "correction" in args:
                correction = args["correction"]
            result[self.analysis_type] = analyses.runCorrelation(self.data, alpha=alpha, method=method, correction=correction)
         
        return result, args

    def get_plot(self, name, identifier, title):
        data = self.result
        args = self.args
        plot = [] 
        if name == "basicTable":
            colors = ('#C2D4FF','#F5F8FF')
            attr =  {'width':800, 'height':300, 'font':12}
            subset = None
            if "colors" in args:
                colors = args["colors"]
            if "attr" in args:
                attr = args["attr"]
            if "subset" in args:
                subset = args["subset"]
            for id in data:
                if isinstance(id, tuple):
                    identifier = identifier+"_"+id[0]+"_vs_"+id[1]
                    figure_title = title + id[0]+" vs "+id[1]
                else:
                    figure_title = title
                plot.append(figure.getBasicTable(data[id], identifier, figure_title, colors=colors, subset=subset, plot_attr=attr))
        elif name == "basicBarPlot":
            x_title = "x"
            y_title = "y"
            if "x_title" in args:
                x_title = args["x_title"]
            if "y_title" in args:
                y_title = args["y_title"]
            for id in data:     
                if isinstance(id, tuple):
                    identifier = identifier+"_"+id[0]+"_vs_"+id[1]
                    figure_title = title + id[0]+" vs "+id[1]
                else:
                    figure_title = title
                plot.append(figure.getBarPlotFigure(data[id], identifier, figure_title, x_title, y_title))
        elif name == "scatterPlot":
            x_title = "x"
            y_title = "y"
            if "x_title" in args:
                x_title = args["x_title"]
            if "y_title" in args:
                y_title = args["y_title"]
            for id in data:
                if isinstance(id, tuple):
                    identifier = identifier+"_"+id[0]+"_vs_"+id[1]
                    figure_title = title + id[0]+" vs "+id[1]
                else:
                    figure_title = title
                plot.append(figure.getScatterPlotFigure(data[id], identifier, figure_title, x_title, y_title))
        elif name == "volcanoPlot":
            alpha = 0.05
            lfc = 1.0
            if "alpha" in args:
                alpha = args["alpha"]
            if "lfc" in args:
                lfc = args["lfc"]
            for pair in data:
                signature = data[pair]
                p = figure.runVolcano(identifier+"_"+pair[0]+"_vs_"+pair[1], signature, lfc=lfc, alpha=alpha, title=title+" "+pair[0]+" vs "+pair[1])
                plot.append(p)
        elif name == '3Dnetwork':
            source = 'source'
            target = 'target'
            if "source" in args:
                source = args["source"]
            if "target" in args:
                target = args["target"]
            for id in data:
                if isinstance(id, tuple):
                    identifier = identifier+"_"+id[0]+"_vs_"+id[1]
                    figure_title = title + id[0]+" vs "+id[1]
                else:
                    figure_title = title
                plot.append(figure.get3DNetworkFigure(data[id], sourceCol=source, targetCol=target, node_properties={}, identifier=identifier, title=figure_title))
        elif name == "heatmap":
            for id in data:
                if not data[id].empty:
                    if isinstance(id, tuple):
                        identifier = identifier+"_"+id[0]+"_vs_"+id[1]
                        figure_title = title + id[0]+" vs "+id[1]
                    else:
                        figure_title = title
                    plot.append(figure.getComplexHeatmapFigure(data[id], identifier=identifier, title=figure_title))
        elif name == "mapper":
            for id in data:
                labels = {}
                if "labels" in args:
                    labels = args["labels"]
                if isinstance(id, tuple):
                    identifier = identifier+"_"+id[0]+"_vs_"+id[1]
                    figure_title = title + id[0]+" vs "+id[1]
                else:
                    figure_title = title
                plot.append(figure.getMapperFigure(data[id], identifier, title=figure_title, labels=args["labels"]))

        return plot