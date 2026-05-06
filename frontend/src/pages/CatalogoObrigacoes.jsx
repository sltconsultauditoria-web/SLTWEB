import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, BookOpen, Filter, AlertCircle, ListChecks, Scale, Link as LinkIcon } from 'lucide-react';
import { api } from '@/context/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

const normalizeList = (payload) => {
  if (Array.isArray(payload)) return payload;
  if (Array.isArray(payload?.data)) return payload.data;
  if (Array.isArray(payload?.catalogo)) return payload.catalogo;
  if (Array.isArray(payload?.obrigacoes)) return payload.obrigacoes;
  return [];
};

const CatalogoObrigacoes = () => {
  const navigate = useNavigate();
  const [catalogo, setCatalogo] = useState([]);
  const [search, setSearch] = useState('');
  const [regime, setRegime] = useState('todos');
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const response = await api.get('/obrigacoes/catalogo');
        setCatalogo(normalizeList(response.data));
      } catch (error) {
        setCatalogo([]);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const filtered = useMemo(() => {
    const term = search.trim().toLowerCase();
    return catalogo.filter((item) => {
      const matchesRegime = regime === 'todos' || (item.regimes || []).includes(regime);
      const matchesTerm =
        !term ||
        String(item.codigo || '').toLowerCase().includes(term) ||
        String(item.nome || '').toLowerCase().includes(term) ||
        String(item.orgao_responsavel || '').toLowerCase().includes(term);
      return matchesRegime && matchesTerm;
    });
  }, [catalogo, regime, search]);

  const regimes = [
    { value: 'todos', label: 'Todos' },
    { value: 'lucro_real', label: 'Lucro Real' },
    { value: 'lucro_presumido', label: 'Lucro Presumido' },
    { value: 'simples_nacional', label: 'Simples Nacional' },
  ];

  return (
    <div className="space-y-6" data-testid="catalogo-obrigacoes-page">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Catálogo Fiscal</h1>
          <p className="text-gray-500">Catálogo completo de obrigações acessórias com regras e integrações</p>
        </div>
        <Button variant="outline" onClick={() => navigate('/obrigacoes')}>
          <BookOpen className="h-4 w-4 mr-2" />
          Obrigações
        </Button>
      </div>

      <Card>
        <CardContent className="p-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            <div className="relative md:col-span-2">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
              <Input
                className="pl-10"
                placeholder="Buscar por nome, código ou órgão"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
              />
            </div>
            <Select value={regime} onValueChange={setRegime}>
              <SelectTrigger>
                <Filter className="h-4 w-4 mr-2 text-gray-400" />
                <SelectValue placeholder="Filtrar por regime" />
              </SelectTrigger>
              <SelectContent>
                {regimes.map((item) => (
                  <SelectItem key={item.value} value={item.value}>
                    {item.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {loading ? (
        <div className="flex items-center justify-center h-48">
          <div className="h-10 w-10 animate-spin rounded-full border-b-2 border-blue-900" />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {filtered.map((item) => (
            <Card key={item.codigo} className="hover:shadow-md transition-shadow">
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <CardTitle className="text-base">{item.nome}</CardTitle>
                    <p className="text-xs text-gray-500 mt-1">{item.codigo}</p>
                  </div>
                  <Badge className="bg-blue-600">{item.periodicidade}</Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                <p className="text-sm text-gray-600 line-clamp-3">{item.descricao}</p>
                <div className="flex flex-wrap gap-2">
                  {(item.regimes || []).slice(0, 3).map((r) => (
                    <Badge key={r} variant="outline">{r}</Badge>
                  ))}
                </div>
                <div className="flex items-center justify-between text-xs text-gray-500">
                  <span>{item.orgao_responsavel}</span>
                  <Button size="sm" variant="outline" onClick={() => setSelected(item)}>
                    Ver detalhes
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
          {filtered.length === 0 && (
            <div className="col-span-full rounded-lg border border-dashed p-10 text-center text-gray-500">
              Nenhuma obrigação encontrada para os filtros aplicados.
            </div>
          )}
        </div>
      )}

      <Dialog open={Boolean(selected)} onOpenChange={(open) => !open && setSelected(null)}>
        <DialogContent className="max-w-3xl">
          <DialogHeader>
            <DialogTitle>{selected?.nome}</DialogTitle>
          </DialogHeader>
          {selected && (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card>
                  <CardContent className="p-4 space-y-2">
                    <div className="flex items-center gap-2 text-sm font-medium"><ListChecks className="h-4 w-4" /> Campos obrigatórios</div>
                    <ul className="space-y-1 text-sm text-gray-600">
                      {(selected.campos || []).map((field) => (
                        <li key={field.nome}>• {field.nome} {field.obrigatorio ? '(obrigatório)' : ''}</li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="p-4 space-y-2">
                    <div className="flex items-center gap-2 text-sm font-medium"><Scale className="h-4 w-4" /> Penalidades</div>
                    <ul className="space-y-1 text-sm text-gray-600">
                      {(selected.penalidades || []).map((item) => (
                        <li key={item}>• {item}</li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              </div>
              <Card>
                <CardContent className="p-4 space-y-2">
                  <div className="flex items-center gap-2 text-sm font-medium"><AlertCircle className="h-4 w-4" /> Regras e integrações</div>
                  <p className="text-sm text-gray-600">{selected.prazo_regra}</p>
                  <p className="text-sm text-gray-600">{selected.multa_atraso}</p>
                  <div className="flex flex-wrap gap-2">
                    {(selected.integracoes || []).map((item) => (
                      <Badge key={item} variant="outline" className="gap-1">
                        <LinkIcon className="h-3 w-3" />
                        {item}
                      </Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default CatalogoObrigacoes;
