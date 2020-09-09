class Util:

    @staticmethod
    def paginatedDisplay(recordList, page):
        indices = Util.getIndices(len(recordList), page)
        return recordList[indices[0]: indices[1]]
    
    @staticmethod
    def getIndices(listSize, page):
        if (page == 0):
            return (0, listSize)
        firstIndex = (page - 1) * 5
        if (listSize < firstIndex or page <= 0):
            return (0, 0)
        lastIndex = firstIndex + 5
        if (listSize < lastIndex):
            lastIndex = listSize
        return (firstIndex, lastIndex)