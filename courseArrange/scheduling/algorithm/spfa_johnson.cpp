#include <cstring>
#include <queue>
#include <algorithm>
using namespace std;

class Network {
public:
    typedef int VAL;    // ·ÑÓÃµÄÀàÐÍ
    static const int SIZE = 1005;       // ×î´óµãÊý
    static const int INF = 1000000007;  // Á÷Á¿µÄ¼«´óÖµ
    typedef struct ARC{int t,c; VAL w; ARC* o;}* PTR;
    ARC arc[200005];    // ×î´ó±ßÊý£¬×¢ÒâÒ»´ÎÆÕÍ¨¼Ó±ß²Ù×÷ÐèÒªÕ¼ÓÃÁ½Ìõ±ß
    PTR now[SIZE],e[SIZE];      // cnt[]Îª¸Ã²ã´ÎÏÂµÄµãÊý£¬l[]Îª²ã´Î±êºÅ
    int cnt[SIZE],l[SIZE],r[SIZE],edge; // now[]Îªµ±Ç°»¡£¬e[]Îª³ö±ßÁ´±í
    VAL sum;   // sumÎªµ±Ç°Á÷ÍøÂçÏÂµÄ·ÑÓÃ
    void clear(){memset(e,edge=sum=0,sizeof(e));}           // Çå¿Õ±ß±í
    ARC& REV(PTR x){return arc[(x-arc)^1];}                 // È¡·´Ïò±ß
    // ´«ÈëÔ´µãSºÍ»ãµãT£¬·µ»ØÁ÷Á¿£¬´¦Àí·ÑÓÃÁ÷Ê±°ÑÏÂÃæ¸Ä³Éspfa_johnson
    int flow(int S, int T){return improved_sap(S,T,INF);}
    // ¼ÓÈëÒ»Ìõxµ½yµÄÓÐÏò±ß£¬ÈÝÁ¿Îªc£¬·ÑÓÃÎªw
    PTR add_edge(int x, int y, int c, VAL w = 0){
        e[x]=&(arc[edge++]=(ARC){y,c,+w,e[x]});
        e[y]=&(arc[edge++]=(ARC){x,0,-w,e[y]});
        return e[x];
    }
    // ¼ÓÈëÒ»Ìõxµ½yµÄÎÞÏò±ß£¬ÈÝÁ¿Îªc£¬·ÑÓÃÎª0
    PTR add_edge_simple(int x, int y, int c){
        e[x]=&(arc[edge++]=(ARC){y,c,0,e[x]});
        e[y]=&(arc[edge++]=(ARC){x,c,0,e[y]});
        return e[x];
    }
    // ¼ÓÈëÒ»Ìõxµ½yµÄÓÐÏò±ß£¬ÏÂ½çÎªlo£¬ÉÏ½çÎªhi£¬·ÑÓÃÎªw
    // ³¬¼¶Ô´ÔÚSIZE-2£¬³¬¼¶»ãÔÚSIZE-1£¬×¢Òâ¸øÕâÁ½¸öµãÔ¤Áô¿Õ¼ä
    PTR add_edge_bounded(int x, int y, int lo, int hi, VAL w = 0){
        add_edge(SIZE-2,y,lo,w);
        add_edge(x,SIZE-1,lo,0);
        return add_edge(x,y,hi-lo,w);
    }
    // ¶ÔSÖÁTÇÒ³ö»¡Îªnow[]µÄÔö¹ãÂ·½øÐÐËÉ³Ú£¬·µ»Ø±»×èÈûµÄ½áµã
    int aug(int S, int T, int& can){
        int x,z=T,use=can;
        for(x=S;x!=T;x=now[x]->t) if(use>now[x]->c) use=now[z=x]->c;
        for(x=S;x!=T;x=now[x]->t){
                now[x]->c-=use;
            REV(now[x]).c+=use;
            sum+=use*now[x]->w;
        }
        can-=use;
        return z;
    }
    // ÎÞÈ¨Öµ×î¶ÌÂ·Ôö¹ãËã·¨£¬ÓÃÔÚÎÞ·ÑÓÃµÄÍøÂçÁ÷ÉÏ£¬·µ»ØÁ÷Á¿
    int improved_sap(int S, int T, int can){ // canÎª±¾´ÎÔö¹ãµÄÁ÷Á¿ÉÏÏÞ
        if(S==T) return can;
        int in=can,x,m;
        memcpy(now,e,sizeof(now));
        memset(cnt,0,sizeof(cnt));
        fill_n(l,SIZE,int(SIZE));
        for(int i=m=l[r[0]=T]=0;i<=m;i++){
            cnt[l[x=r[i]]]++;
            for(PTR u=e[x];u;u=u->o)
                if(l[u->t]==SIZE && REV(u).c) l[r[++m]=u->t]=l[x]+1;
        }
        for(x=r[S]=S;l[S]!=SIZE;x=r[x]){
        JMP:for(PTR& u=now[x];u;u=u->o) if(l[u->t]<l[x] && u->c){
                r[u->t]=x;
                x=u->t==T?aug(S,T,can):u->t;
                if(x==T) return in; else goto JMP;
            }
            if(!--cnt[l[x]]) break; else l[x]=SIZE;
            for(PTR u=e[x];u;u=u->o)
                if(l[u->t]+1<l[x] && u->c) now[x]=u,l[x]=l[u->t]+1;
            if(l[x]!=SIZE) cnt[l[x]]++;
        }
        return in-can;
    }
    // Á¬Ðø×î¶ÌÂ·Ôö¹ãËã·¨£¬¿ÉÒÔ´¦Àí²»º¬¸º·ÑÓÃÈ¦µÄ·ÑÓÃÁ÷£¬·µ»ØÁ÷Á¿
    int spfa_johnson(int S, int T, int can){ // canÎª±¾´ÎÔö¹ãµÄÁ÷Á¿ÉÏÏÞ
        if(S==T) return can;
        int in=can,x,m;
        VAL phi[SIZE],len[SIZE],MAXW=1000000007; // ·ÑÓÃµÄ¼«´óÖµ
        memset(l,0,sizeof(l));
        fill_n(phi,SIZE,MAXW);
        phi[r[0]=T]=0;
        for(int i=m=0;i<=m;i++){ // ´Ó»ãµã³ö·¢·´ÏòSPFA
            l[x=r[i%SIZE]]=0;
            for(PTR u=e[x];u;u=u->o){ // ÏÂÃæÕâÐÐÈç¹ûÊÇ¸¡µã±È½ÏÒª¼ÓEPS
                if(phi[x]+REV(u).w>=phi[u->t] || !REV(u).c) continue;
                phi[u->t]=phi[x]+REV(u).w;
                if(!l[u->t]) l[r[++m%SIZE]=u->t]=1;
            }
        }
        do{
            typedef pair<VAL,int> TPL;
            priority_queue<TPL> q;
            fill_n(len,SIZE,MAXW);
            memset(l,0,sizeof(l));
            q.push(TPL(len[T]=0,T));
            while(q.size()){
                x=q.top().second; q.pop();
                if(!l[x]) l[x]=1; else continue;
                for(PTR u=e[x];u;u=u->o){
                    if(!REV(u).c || l[u->t]) continue;
                    VAL at=len[x]+phi[x]+REV(u).w-phi[u->t];
                    if(at>=len[u->t]) continue; // Èç¹ûÊÇ¸¡µã±È½ÏÒª¼ÓEPS
                    len[u->t]=at;
                    now[u->t]=&REV(u);
                    q.push(TPL(-at,u->t));
                }
            }
            for(x=0;x<SIZE;x++) phi[x]+=len[x];
        }while(phi[S]<MAXW && aug(S,T,can)!=T);
        // Ê¹ÓÃphi[S]<MAXWÇó×îÐ¡·ÑÓÃ×î´óÁ÷£¬Ê¹ÓÃphi[S]<0Çó×îÐ¡·ÑÓÃÁ÷
        return in-can;
    }
    // ÅÐ¶ÏÎÞÔ´»ãÉÏÏÂ½ç¿ÉÐÐÁ÷ÊÇ·ñ´æÔÚ
    // ¼ÓÈë±ß(T,S)=MAXF¿É´¦Àí´øÔ´»ãµÄÇé¿ö£¬´ËÊ±·´Ïò»¡S->TµÄc¼´ÎªÁ÷Á¿
    bool feasible_bounded(){
        flow(SIZE-2,SIZE-1);
        for(PTR u=e[SIZE-2];u;u=u->o) if(u->c) return false;
        return true;
    }
    // ÓÐÔ´»ãÉÏÏÂ½ç×î´ó/×îÐ¡Á÷£¬·µ»Ø-1±íÊ¾²»´æÔÚ¿ÉÐÐÁ÷£¬·ñÔò·µ»ØÁ÷Á¿
    int max_flow_bounded(int S, int T){
        add_edge(T,S,INF);
        bool ok=feasible_bounded();
        int ret=e[S]->c;
        edge-=2,e[S]=e[S]->o,e[T]=e[T]->o;
        return ok?ret+flow(S,T):-1;
    }
    int min_flow_bounded(int S, int T){
        flow(SIZE-2,SIZE-1);
        add_edge(T,S,INF);
        bool ok=feasible_bounded();
        int ret=e[S]->c;
        edge-=2,e[S]=e[S]->o,e[T]=e[T]->o;
        return ok?ret:-1;
    }
    // ½«ËùÓÐ´øÏÂ½çµÄ±ßºÏ²¢»ØÔ­Í¼ÖÐ
    void merge_bounded(){
        for(PTR u=e[SIZE-1];u;u=u->o) u->c=REV(u).c=0;
        for(PTR u=e[SIZE-2];u;u=u->o){
            (u+4)->c+=u->c;
            (u+5)->c+=REV(u).c;
            u->c=REV(u).c=0;
        }
    }
};
