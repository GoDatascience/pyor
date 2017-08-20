urnas = function(ret, rept) {

    bolas=c()
    cvd=8
    cvm=2

    ma=matrix(1, nrow=rept, ncol=ret)
    soma=c()

    for(j in 1:rept){
        set_progress(j/rept)
        for(i in 1:ret){
            s=sample(1:cvd+cvm, 1, rep = T)
            if(1<s && s<=cvd){
                y1=rgeom(1,2/10)+1
                bolas[i]=1
                cvd=cvd+y1-1
                cvm=cvm+1
            } else{
                y1=rgeom(1,8/10)+1
                bolas[i]=0
                cvm=cvm+y1-1
                cvd=cvd+1
            }

        }
        ma[j,]=bolas
        soma[j]=sum(bolas)
    }

    mean(soma)
}

urnas(params[["ret"]],params[["rept"]])