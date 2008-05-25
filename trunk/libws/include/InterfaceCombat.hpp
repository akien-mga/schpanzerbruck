#ifndef INTERFACE_COMBAT_HEADER
#define INTERFACE_COMBAT_HEADER

#include "GestionnaireImages.hpp"

#include <SFML/Graphics.hpp>
#include <GL/gl.h>
#include <GL/glu.h>

#include <string>

using namespace std;


namespace ws
{

class InterfaceCombat
{
private:
    bool menuEchapON, barreInfosON, clic;
    
    unsigned int appL, appH;
    GestionnaireImages* gestImages;
    
    int picked[2];
    
    void GL_LigneTexte(string texte, float largeurTxt, float hauteurTxt, unsigned int numPoliceBmp=1);
    void GL_LigneTexteLargeurMax(string texte, float largeurTxtMax, float hauteurTxt, bool centrer=true, unsigned int numPoliceBmp=1);
    void GL_LigneTexteHauteurMax(string texte, float largeurTxt, float hauteurTxtMax, bool centrer=true, unsigned int numPoliceBmp=1);
    
    void GL_Cadre(float L, float H, float offset=0);
    
    void GL_Bouton(string texte, int R_txt, int V_txt, int B_txt, float L, float H, float offset=0);
    
    void GL_MenuEchapPourSelection();
    void GL_MenuEchap();
    
    void GL_BarreInfos();
    
    unsigned int factAssomb;
    string infosActDsBarre[3];
    
public:
    enum {
        SLC_CONTINUER, SLC_QUITTER, SLC_MENU_ECHAP,
        SLC_MENU_TRIANGLE, SLC_DEPLACEMENT, SLC_ACTION, SLC_FIN_DU_TOUR
    };
    
    int mtrChoisies[3];
    
    InterfaceCombat(GestionnaireImages* _gestImages, unsigned int _appL, unsigned int _appH);
    
    void switchMenuEchap();
    
    void GL_DessinPourSelection(unsigned int curseurX, unsigned int curseurY, bool _clic=false);
    void GL_Dessin();
    
    void passerSelection(int* selection);
    void pasDeSelection();
    void setInfosDsBarre(string tuile="", string element="", string perso="");
};

}

#endif